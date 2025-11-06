"""Tests for the HUD class."""

import pygame
import pytest
from hud import HUD
from warrior import Warrior
import config


@pytest.fixture
def hud():
    """Create a HUD instance for testing."""
    pygame.init()
    return HUD()


@pytest.fixture
def warrior():
    """Create a warrior instance for testing."""
    return Warrior(0, 0)


def test_hud_initialization(hud):
    """Test that HUD initializes with correct default values."""
    assert hud.displayed_health == 0
    assert hud.animation_speed == 2.0
    assert hud.potion_glow_timer == 0
    assert hud.critical_health_timer == 0
    assert hud.critical_health_threshold == 0.25


def test_hud_update_initializes_health(hud, warrior):
    """Test that HUD initializes displayed health on first update."""
    assert hud.displayed_health == 0
    hud.update(warrior, 0.1)
    # After initialization, displayed health should be set to warrior health
    # Since we use animation, it should be initialized and moving toward target
    assert hud.displayed_health > 0
    assert hud.displayed_health <= warrior.health


def test_hud_update_animates_health_increase(hud, warrior):
    """Test that HUD animates health bar when health increases."""
    hud.displayed_health = 50
    warrior.health = 80

    # After one update, displayed health should be closer to target
    hud.update(warrior, 0.1)
    assert hud.displayed_health > 50
    assert hud.displayed_health <= 80


def test_hud_update_animates_health_decrease(hud, warrior):
    """Test that HUD animates health bar when health decreases."""
    hud.displayed_health = 80
    warrior.health = 50

    # After one update, displayed health should be closer to target
    hud.update(warrior, 0.1)
    assert hud.displayed_health < 80
    assert hud.displayed_health >= 50


def test_hud_potion_glow_trigger(hud):
    """Test that potion glow can be triggered."""
    assert hud.potion_glow_timer == 0
    hud.trigger_potion_glow()
    assert hud.potion_glow_timer == hud.potion_glow_duration


def test_hud_potion_glow_timer_decreases(hud, warrior):
    """Test that potion glow timer decreases over time."""
    hud.trigger_potion_glow()
    initial_timer = hud.potion_glow_timer

    hud.update(warrior, 0.1)
    assert hud.potion_glow_timer < initial_timer


def test_hud_critical_health_warning_activated(hud, warrior):
    """Test that critical health warning activates when health is low."""
    warrior.health = 20  # 20% of max health

    hud.update(warrior, 0.1)
    assert hud.critical_health_timer > 0


def test_hud_critical_health_warning_not_activated(hud, warrior):
    """Test that critical health warning doesn't activate when health is normal."""
    warrior.health = 80

    hud.update(warrior, 0.1)
    assert hud.critical_health_timer == 0


def test_hud_critical_health_warning_deactivates(hud, warrior):
    """Test that critical health warning deactivates when health increases."""
    warrior.health = 20  # Low health
    hud.update(warrior, 0.1)
    assert hud.critical_health_timer > 0

    warrior.health = 80  # Health restored
    hud.update(warrior, 0.1)
    assert hud.critical_health_timer == 0


def test_hud_draw_does_not_crash(hud, warrior):
    """Test that HUD draw method doesn't crash."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_draw_with_critical_health(hud, warrior):
    """Test that HUD draws correctly with critical health."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 20
    hud.update(warrior, 0.1)

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_draw_with_potion_glow(hud, warrior):
    """Test that HUD draws correctly with potion glow effect."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    hud.trigger_potion_glow()

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_colors_defined(hud):
    """Test that all HUD colors are properly defined."""
    assert hud.wood_color is not None
    assert hud.wood_border is not None
    assert hud.ornate_gold is not None
    assert hud.health_green is not None
    assert hud.health_red is not None
    assert hud.health_critical is not None
    assert hud.text_color is not None


def test_hud_health_animation_converges(hud, warrior):
    """Test that health animation converges to target over multiple updates."""
    hud.displayed_health = 100
    warrior.health = 50

    # Animate over multiple frames
    for _ in range(100):
        hud.update(warrior, 0.1)

    # Should be very close to target
    assert abs(hud.displayed_health - warrior.health) < 1.0


def test_hud_draw_with_zero_health(hud, warrior):
    """Test that HUD draws correctly when health is zero."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 0
    hud.displayed_health = 0

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_draw_with_no_potions(hud, warrior):
    """Test that HUD draws correctly when no potions available."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health_potions = 0

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_draw_with_no_gold(hud, warrior):
    """Test that HUD draws correctly when no gold available."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.gold = 0

    # Should not raise any exceptions
    hud.draw(screen, warrior)


def test_hud_critical_health_warning_displays_correctly(hud, warrior):
    """Test critical health warning cycles through display states."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 20

    # Update multiple times to cycle through warning states
    for _ in range(10):
        hud.update(warrior, 0.5)
        hud.draw(screen, warrior)

    # Should have accumulated timer
    assert hud.critical_health_timer > 0


def test_hud_update_caps_health_animation(hud, warrior):
    """Test that health animation doesn't exceed bounds."""
    # Test upper bound
    hud.displayed_health = 95
    warrior.health = 100
    hud.update(warrior, 10.0)  # Large dt to force overshoot
    assert hud.displayed_health <= warrior.max_health

    # Test lower bound
    hud.displayed_health = 5
    warrior.health = 0
    hud.update(warrior, 10.0)  # Large dt to force undershoot
    assert hud.displayed_health >= 0


def test_hud_draw_with_high_health(hud, warrior):
    """Test HUD draws with health > 50% (green bar)."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 80
    hud.displayed_health = 80

    # Should not raise any exceptions and should draw green bar
    hud.draw(screen, warrior)


def test_hud_draw_with_medium_health(hud, warrior):
    """Test HUD draws with health between 25% and 50% (yellow bar)."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 40
    hud.displayed_health = 40

    # Should not raise any exceptions and should draw yellow bar
    hud.draw(screen, warrior)


def test_hud_draw_with_low_health(hud, warrior):
    """Test HUD draws with health < 25% (red bar)."""
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    warrior.health = 20
    hud.displayed_health = 20

    # Should not raise any exceptions and should draw red bar
    hud.draw(screen, warrior)


def test_hud_initialization_from_zero_health(hud, warrior):
    """Test HUD initializes displayed_health from zero when warrior has health."""
    # Start with displayed_health at 0
    assert hud.displayed_health == 0
    warrior.health = 100

    # Update should set displayed_health directly to warrior.health on first call
    hud.update(warrior, 0.001)

    # After update, displayed_health should be set to warrior health
    assert hud.displayed_health == warrior.health
