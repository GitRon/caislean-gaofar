"""Tests for AttackEffect and AttackEffectManager classes."""

import pytest
import pygame
from caislean_gaofar.ui.attack_effect import AttackEffect, AttackEffectManager


class TestAttackEffect:
    """Test cases for the AttackEffect class."""

    @pytest.fixture
    def screen(self):
        """Create a test screen surface."""
        pygame.init()
        return pygame.display.set_mode((800, 600))

    def test_attack_effect_initialization(self):
        """Test attack effect initializes with correct attributes."""
        effect = AttackEffect(100, 150, is_crit=False)

        assert effect.x == 100
        assert effect.y == 150
        assert effect.is_crit is False
        assert effect.active is True
        assert effect.effect_time == 0.5
        assert effect.animation_time == 0.0
        assert effect.max_duration == 0.5

    def test_attack_effect_initialization_crit(self):
        """Test critical attack effect initializes correctly."""
        effect = AttackEffect(200, 250, is_crit=True)

        assert effect.x == 200
        assert effect.y == 250
        assert effect.is_crit is True
        assert effect.active is True
        assert effect.effect_time == 0.5

    def test_attack_effect_update(self):
        """Test attack effect updates timing correctly."""
        effect = AttackEffect(100, 100)

        effect.update(0.1)

        assert effect.animation_time == 0.1
        assert effect.effect_time == pytest.approx(0.4)
        assert effect.active is True

    def test_attack_effect_update_multiple_times(self):
        """Test attack effect timing accumulates correctly."""
        effect = AttackEffect(100, 100)

        effect.update(0.1)
        effect.update(0.2)

        assert effect.animation_time == pytest.approx(0.3)
        assert effect.effect_time == pytest.approx(0.2)
        assert effect.active is True

    def test_attack_effect_expires(self):
        """Test attack effect becomes inactive after duration."""
        effect = AttackEffect(100, 100)

        effect.update(0.6)

        assert effect.active is False
        assert effect.effect_time <= 0

    def test_attack_effect_expires_exactly_at_duration(self):
        """Test attack effect expires at exact duration."""
        effect = AttackEffect(100, 100)

        effect.update(0.5)

        assert effect.active is False
        assert effect.effect_time == 0.0

    def test_attack_effect_update_when_inactive(self):
        """Test updating inactive effect does nothing."""
        effect = AttackEffect(100, 100)
        effect.active = False

        initial_time = effect.animation_time
        effect.update(0.1)

        # Should not update when inactive
        assert effect.animation_time == initial_time

    def test_attack_effect_draw_normal(self, screen):
        """Test drawing a normal (non-crit) attack effect."""
        effect = AttackEffect(400, 300, is_crit=False)

        # Should not raise any exceptions
        effect.draw(screen)

    def test_attack_effect_draw_crit(self, screen):
        """Test drawing a critical attack effect."""
        effect = AttackEffect(400, 300, is_crit=True)

        # Should not raise any exceptions
        effect.draw(screen)

    def test_attack_effect_draw_when_inactive(self, screen):
        """Test drawing inactive effect does nothing."""
        effect = AttackEffect(400, 300)
        effect.active = False

        # Should not raise any exceptions and should return early
        effect.draw(screen)

    def test_attack_effect_draw_at_different_progress_levels(self, screen):
        """Test drawing effect at various progress levels."""
        effect = AttackEffect(400, 300)

        # Draw at start
        effect.draw(screen)

        # Draw at 25% progress
        effect.update(0.125)
        effect.draw(screen)

        # Draw at 50% progress
        effect.update(0.125)
        effect.draw(screen)

        # Draw at 75% progress
        effect.update(0.125)
        effect.draw(screen)

        # Draw near end
        effect.update(0.1)
        effect.draw(screen)

    def test_attack_effect_draw_crit_with_impact_lines(self, screen):
        """Test drawing crit effect with impact lines (progress < 0.5)."""
        effect = AttackEffect(400, 300, is_crit=True)

        # Draw when progress is less than 0.5 (impact lines should appear)
        effect.update(0.1)  # progress = 0.2
        effect.draw(screen)

    def test_attack_effect_draw_crit_without_impact_lines(self, screen):
        """Test drawing crit effect without impact lines (progress >= 0.5)."""
        effect = AttackEffect(400, 300, is_crit=True)

        # Draw when progress is >= 0.5 (no impact lines)
        effect.update(0.3)  # progress = 0.6
        effect.draw(screen)

    def test_attack_effect_radius_calculation(self, screen):
        """Test radius calculation at different progress levels."""
        effect = AttackEffect(400, 300, is_crit=False)

        # Normal attack max radius is 25
        effect.update(0.0)  # progress = 0
        effect.draw(screen)

        effect.update(0.25)  # progress = 0.5
        effect.draw(screen)

        effect.update(0.24)  # progress = 0.98
        effect.draw(screen)

    def test_attack_effect_crit_radius_calculation(self, screen):
        """Test crit radius calculation (larger than normal)."""
        effect = AttackEffect(400, 300, is_crit=True)

        # Crit attack max radius is 35
        effect.update(0.25)  # Mid-progress
        effect.draw(screen)

    def test_attack_effect_draw_with_zero_or_negative_radius(self, screen):
        """Test drawing effect handles zero/negative radius in layers."""
        effect = AttackEffect(400, 300)

        # Update to very end to create small/zero radius
        effect.update(0.49)
        effect.draw(screen)

    def test_attack_effect_pulse_animation(self, screen):  # noqa: PBR008
        """Test pulse animation at different time values."""
        effect = AttackEffect(400, 300)

        # Test various animation times to ensure pulse varies
        for time in [0, 0.1, 0.2, 0.3, 0.4]:
            effect.animation_time = time
            effect.draw(screen)

    def test_attack_effect_different_positions(self, screen):  # noqa: PBR008
        """Test effects at various screen positions."""
        positions = [(0, 0), (800, 600), (400, 300), (100, 500)]

        for x, y in positions:
            effect = AttackEffect(x, y)
            effect.draw(screen)

    def test_attack_effect_crit_line_angles(self, screen):
        """Test crit effect draws all 8 directional lines."""
        effect = AttackEffect(400, 300, is_crit=True)

        # Draw at early stage when lines are visible
        effect.update(0.05)
        effect.draw(screen)


class TestAttackEffectManager:
    """Test cases for the AttackEffectManager class."""

    @pytest.fixture
    def screen(self):
        """Create a test screen surface."""
        pygame.init()
        return pygame.display.set_mode((800, 600))

    def test_manager_initialization(self):
        """Test manager initializes with empty effects list."""
        manager = AttackEffectManager()

        assert manager.effects == []

    def test_manager_add_effect(self):
        """Test adding a single effect."""
        manager = AttackEffectManager()

        manager.add_effect(100, 150, is_crit=False)

        assert len(manager.effects) == 1
        assert manager.effects[0].x == 100
        assert manager.effects[0].y == 150
        assert manager.effects[0].is_crit is False

    def test_manager_add_crit_effect(self):
        """Test adding a critical effect."""
        manager = AttackEffectManager()

        manager.add_effect(200, 250, is_crit=True)

        assert len(manager.effects) == 1
        assert manager.effects[0].is_crit is True

    def test_manager_add_multiple_effects(self):
        """Test adding multiple effects."""
        manager = AttackEffectManager()

        manager.add_effect(100, 100)
        manager.add_effect(200, 200)
        manager.add_effect(300, 300, is_crit=True)

        assert len(manager.effects) == 3

    def test_manager_update_single_effect(self):
        """Test updating a single effect."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)

        manager.update(0.1)

        assert manager.effects[0].animation_time == 0.1

    def test_manager_update_multiple_effects(self):
        """Test updating multiple effects."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)
        manager.add_effect(200, 200)

        manager.update(0.2)

        assert manager.effects[0].animation_time == 0.2
        assert manager.effects[1].animation_time == 0.2

    def test_manager_removes_expired_effects(self):
        """Test manager removes expired effects after update."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)

        # Update past effect duration
        manager.update(0.6)

        assert len(manager.effects) == 0

    def test_manager_keeps_active_effects(self):
        """Test manager keeps active effects."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)

        # Update less than effect duration
        manager.update(0.2)

        assert len(manager.effects) == 1
        assert manager.effects[0].active is True

    def test_manager_mixed_active_and_expired_effects(self):
        """Test manager correctly handles mix of active and expired effects."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)
        manager.update(0.3)  # First effect at 0.3s

        manager.add_effect(200, 200)  # Second effect just added

        # Update to expire first but not second
        manager.update(0.3)  # First at 0.6s (expired), second at 0.3s (active)

        assert len(manager.effects) == 1
        assert manager.effects[0].x == 200

    def test_manager_draw_no_effects(self, screen):
        """Test drawing with no effects."""
        manager = AttackEffectManager()

        # Should not raise any exceptions
        manager.draw(screen)

    def test_manager_draw_single_effect(self, screen):
        """Test drawing a single effect."""
        manager = AttackEffectManager()
        manager.add_effect(400, 300)

        # Should not raise any exceptions
        manager.draw(screen)

    def test_manager_draw_multiple_effects(self, screen):
        """Test drawing multiple effects."""
        manager = AttackEffectManager()
        manager.add_effect(300, 200)
        manager.add_effect(400, 300, is_crit=True)
        manager.add_effect(500, 400)

        # Should not raise any exceptions
        manager.draw(screen)

    def test_manager_clear(self):
        """Test clearing all effects."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)
        manager.add_effect(200, 200)
        manager.add_effect(300, 300)

        manager.clear()

        assert len(manager.effects) == 0

    def test_manager_clear_empty_manager(self):
        """Test clearing empty manager."""
        manager = AttackEffectManager()

        manager.clear()

        assert len(manager.effects) == 0

    def test_manager_update_empty_manager(self):
        """Test updating empty manager."""
        manager = AttackEffectManager()

        # Should not raise any exceptions
        manager.update(0.1)

        assert len(manager.effects) == 0

    def test_manager_add_effect_after_clear(self):
        """Test adding effects after clear."""
        manager = AttackEffectManager()
        manager.add_effect(100, 100)
        manager.clear()

        manager.add_effect(200, 200)

        assert len(manager.effects) == 1
        assert manager.effects[0].x == 200

    def test_manager_full_lifecycle(self, screen):
        """Test full lifecycle: add, update, draw, expire."""
        manager = AttackEffectManager()

        # Add effects
        manager.add_effect(300, 300)
        manager.add_effect(400, 400, is_crit=True)
        assert len(manager.effects) == 2

        # Update and draw
        manager.update(0.1)
        manager.draw(screen)
        assert len(manager.effects) == 2

        # Update more
        manager.update(0.2)
        manager.draw(screen)
        assert len(manager.effects) == 2

        # Update to expire
        manager.update(0.5)
        assert len(manager.effects) == 0

    def test_manager_effects_independence(self):
        """Test that effects update independently."""
        manager = AttackEffectManager()

        # Add first effect
        manager.add_effect(100, 100)
        manager.update(0.2)

        # Add second effect
        manager.add_effect(200, 200)

        # First effect should be at 0.2s, second at 0s
        assert manager.effects[0].animation_time == 0.2
        assert manager.effects[1].animation_time == 0.0

        # Update both
        manager.update(0.1)

        assert manager.effects[0].animation_time == pytest.approx(0.3)
        assert manager.effects[1].animation_time == pytest.approx(0.1)

    def test_manager_handles_many_effects(self, screen):  # noqa: PBR008
        """Test manager handles many effects simultaneously."""
        manager = AttackEffectManager()

        # Add many effects
        for i in range(20):
            manager.add_effect(100 + i * 10, 100 + i * 10, is_crit=(i % 3 == 0))

        assert len(manager.effects) == 20

        # Update and draw
        manager.update(0.1)
        manager.draw(screen)

        assert len(manager.effects) == 20

        # Expire all
        manager.update(0.5)
        assert len(manager.effects) == 0
