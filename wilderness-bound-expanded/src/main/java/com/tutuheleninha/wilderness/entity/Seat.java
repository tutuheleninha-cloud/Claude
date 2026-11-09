package com.tutuheleninha.wilderness.entity;

import java.util.List;

import com.tutuheleninha.wilderness.block.LogBenchBlock;
import com.tutuheleninha.wilderness.registry.ModEntities;

import net.minecraft.core.BlockPos;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Invisible entity that players ride while sitting on a bench. It only exists while someone sits on it.
 */
public class Seat extends Entity {
	public Seat(EntityType<? extends Seat> type, Level level) {
		super(type, level);
		this.noPhysics = true;
		this.setNoGravity(true);
	}

	/**
	 * Seats the player on the block at {@code pos}. Returns false when the seat is taken.
	 */
	public static boolean sitDown(ServerLevel level, BlockPos pos, Player player, double height) {
		List<Seat> existing = level.getEntitiesOfClass(Seat.class, new AABB(pos));

		if (!existing.isEmpty()) {
			return false;
		}

		Seat seat = ModEntities.SEAT.create(level, EntitySpawnReason.TRIGGERED);

		if (seat == null) {
			return false;
		}

		seat.setPos(pos.getX() + 0.5, pos.getY() + height, pos.getZ() + 0.5);
		level.addFreshEntity(seat);

		if (!player.startRiding(seat)) {
			seat.discard();
			return false;
		}

		return true;
	}

	@Override
	public void tick() {
		super.tick();

		if (!this.level().isClientSide()) {
			boolean onBench = this.level().getBlockState(this.blockPosition()).getBlock() instanceof LogBenchBlock;

			if (!this.isVehicle() || !onBench) {
				this.ejectPassengers();
				this.discard();
			}
		}
	}

	@Override
	protected Vec3 getPassengerAttachmentPoint(Entity passenger, EntityDimensions dimensions, float scale) {
		return Vec3.ZERO;
	}

	@Override
	public Vec3 getDismountLocationForPassenger(LivingEntity passenger) {
		BlockPos pos = this.blockPosition();
		return new Vec3(pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5);
	}

	@Override
	protected void defineSynchedData(SynchedEntityData.Builder builder) {
	}

	@Override
	public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
		return false;
	}

	@Override
	public boolean shouldBeSaved() {
		return false;
	}

	@Override
	protected void readAdditionalSaveData(ValueInput input) {
	}

	@Override
	protected void addAdditionalSaveData(ValueOutput output) {
	}
}
