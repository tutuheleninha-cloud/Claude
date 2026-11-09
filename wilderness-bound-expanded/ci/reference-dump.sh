#!/usr/bin/env bash
# Development helper used by CI: dumps API *signatures* (javap -p, no method bodies) of the
# Minecraft 26.3 / Fabric API jars so the mod can be written against the exact names of
# this version. Output goes to $1/reference.
set -uo pipefail

OUT="$1/reference"
mkdir -p "$OUT"

./gradlew -q printClientClasspath | grep '^CP ' | sed 's/^CP //' > "$OUT/classpath.txt"

: > "$OUT/mc-jars.txt"
while read -r jar; do
	[[ "$jar" == *.jar ]] || continue
	if unzip -Z1 "$jar" 2>/dev/null | grep -q '^net/minecraft/'; then
		echo "$jar" >> "$OUT/mc-jars.txt"
	fi
done < "$OUT/classpath.txt"

: > "$OUT/mc-classes.txt"
: > "$OUT/javap-mc.txt"
while read -r jar; do
	unzip -Z1 "$jar" | grep '\.class$' | sed 's/\.class$//' | sort > "$OUT/tmp-classes.txt"
	cat "$OUT/tmp-classes.txt" >> "$OUT/mc-classes.txt"
	grep -E '^(net/minecraft|com/mojang)/' "$OUT/tmp-classes.txt" | tr '/' '.' > "$OUT/tmp-names.txt"
	split -l 300 "$OUT/tmp-names.txt" "$OUT/chunk_"
	for chunk in "$OUT"/chunk_*; do
		# shellcheck disable=SC2046
		javap -p -cp "$jar" $(cat "$chunk") >> "$OUT/javap-mc.txt" 2>/dev/null || true
		rm -f "$chunk"
	done
done < "$OUT/mc-jars.txt"
rm -f "$OUT/tmp-classes.txt" "$OUT/tmp-names.txt"
gzip -9 -f "$OUT/javap-mc.txt"

# Fabric API class list (sources are read from GitHub; this only maps class -> module)
while read -r jar; do
	[[ "$jar" == *.jar ]] || continue
	case "$jar" in
		*fabric*)
			echo "## $jar"
			unzip -Z1 "$jar" | grep '\.class$' | grep -v '/impl/\|/mixin/' ;;
	esac
done < "$OUT/classpath.txt" > "$OUT/fabric-classes.txt"

# Bytecode (javap -c) for the few classes whose structure matters for mixins.
if [ -f ci/javap-c.txt ]; then
	: > "$OUT/javap-c.txt"
	while read -r cls; do
		[ -z "$cls" ] && continue
		while read -r jar; do
			javap -p -c -cp "$jar" "$cls" >> "$OUT/javap-c.txt" 2>/dev/null && break
		done < "$OUT/mc-jars.txt"
	done < ci/javap-c.txt
	gzip -9 -f "$OUT/javap-c.txt"
fi

ls -la "$OUT"
