"""Skill selection and management UI."""

import pygame
import config
from skills import WARRIOR_SKILLS, SkillType


class SkillUI:
    """UI for viewing and selecting warrior skills."""

    def __init__(self):
        """Initialize the skill UI."""
        self.panel_width = 500
        self.panel_height = 450
        self.panel_x = (config.SCREEN_WIDTH - self.panel_width) // 2
        self.panel_y = (config.SCREEN_HEIGHT - self.panel_height) // 2

        # Colors
        self.bg_color = (30, 30, 40)
        self.border_color = (218, 165, 32)  # Gold
        self.text_color = (255, 248, 220)
        self.locked_color = (100, 100, 100)
        self.learned_color = (50, 200, 50)
        self.available_color = (255, 215, 0)

        # Skill selection state
        self.selected_skill_id = None
        self.hovered_skill_id = None

    def draw(self, screen: pygame.Surface, warrior):
        """
        Draw the skill UI.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Draw main panel
        panel_rect = pygame.Rect(
            self.panel_x, self.panel_y, self.panel_width, self.panel_height
        )
        pygame.draw.rect(screen, self.bg_color, panel_rect)
        pygame.draw.rect(screen, self.border_color, panel_rect, 3)

        # Draw title
        font_title = pygame.font.Font(None, 36)
        title_text = font_title.render("Skill Tree", True, self.border_color)
        screen.blit(title_text, (self.panel_x + 20, self.panel_y + 15))

        # Draw level and skill points info
        font_info = pygame.font.Font(None, 24)
        level_text = font_info.render(
            f"Level: {warrior.experience.current_level}", True, self.text_color
        )
        skill_points = warrior.experience.get_available_skill_points()
        points_text = font_info.render(
            f"Skill Points: {skill_points}", True, self.available_color
        )
        screen.blit(level_text, (self.panel_x + 20, self.panel_y + 55))
        screen.blit(points_text, (self.panel_x + 200, self.panel_y + 55))

        # Draw skills organized by tier
        self._draw_skill_tree(screen, warrior)

        # Draw instructions
        font_hint = pygame.font.Font(None, 20)
        hint_text = font_hint.render(
            "Press K to close | Click to learn skill | Right-click to set active",
            True,
            config.GRAY,
        )
        screen.blit(
            hint_text,
            (self.panel_x + 20, self.panel_y + self.panel_height - 30),
        )

    def _draw_skill_tree(self, screen: pygame.Surface, warrior):
        """
        Draw the skill tree with tiers.

        Args:
            screen: Pygame surface to draw on
            warrior: The warrior entity
        """
        start_y = self.panel_y + 90
        skill_height = 60
        skill_spacing = 10

        current_level = warrior.experience.current_level

        # Draw each tier
        for tier in range(1, 6):  # Tiers 1-5
            tier_y = start_y + (tier - 1) * (skill_height + skill_spacing)

            # Draw tier label
            font_tier = pygame.font.Font(None, 22)
            tier_label = font_tier.render(
                f"Tier {tier} (Level {tier + 1})", True, self.border_color
            )
            screen.blit(tier_label, (self.panel_x + 20, tier_y))

            # Get skills for this tier
            tier_skills = [
                (skill_id, skill)
                for skill_id, skill in WARRIOR_SKILLS.items()
                if skill.tier == tier
            ]

            # Draw skills side by side
            skill_x = self.panel_x + 150
            skill_width = 150
            for i, (skill_id, skill) in enumerate(tier_skills):
                skill_rect = pygame.Rect(
                    skill_x + i * (skill_width + 10),
                    tier_y,
                    skill_width,
                    skill_height,
                )

                # Determine skill state
                is_learned = skill_id in warrior.skills.learned_skills
                is_locked = current_level < tier + 1
                is_active = warrior.skills.active_skill == skill_id

                # Draw skill box
                if is_locked:
                    color = self.locked_color
                elif is_learned:
                    color = self.learned_color
                elif warrior.experience.get_available_skill_points() > 0:
                    color = self.available_color
                else:
                    color = self.border_color

                pygame.draw.rect(screen, color, skill_rect, 2)

                # Highlight if hovered
                mouse_pos = pygame.mouse.get_pos()
                if skill_rect.collidepoint(mouse_pos):
                    self.hovered_skill_id = skill_id
                    hover_overlay = pygame.Surface((skill_width, skill_height))
                    hover_overlay.set_alpha(50)
                    hover_overlay.fill((255, 255, 255))
                    screen.blit(hover_overlay, (skill_rect.x, skill_rect.y))

                # Draw skill icon (colored circle)
                icon_radius = 15
                icon_x = skill_rect.x + 20
                icon_y = skill_rect.y + 20
                pygame.draw.circle(screen, skill.icon_color, (icon_x, icon_y), icon_radius)

                # Draw skill name
                font_skill = pygame.font.Font(None, 18)
                skill_name = skill.name
                # Truncate long names
                if len(skill_name) > 12:
                    skill_name = skill_name[:12] + "..."

                name_text = font_skill.render(skill_name, True, self.text_color)
                screen.blit(name_text, (skill_rect.x + 45, skill_rect.y + 5))

                # Draw skill type
                font_type = pygame.font.Font(None, 14)
                type_color = (255, 100, 100) if skill.skill_type == SkillType.ACTIVE else (100, 255, 100)
                type_text = font_type.render(
                    skill.skill_type.value.upper(), True, type_color
                )
                screen.blit(type_text, (skill_rect.x + 45, skill_rect.y + 25))

                # Draw status indicators
                status_y = skill_rect.y + 43
                if is_active:
                    status_text = font_type.render("[ACTIVE]", True, (255, 215, 0))
                    screen.blit(status_text, (skill_rect.x + 45, status_y))
                elif is_learned:
                    status_text = font_type.render("LEARNED", True, self.learned_color)
                    screen.blit(status_text, (skill_rect.x + 45, status_y))
                elif is_locked:
                    status_text = font_type.render("LOCKED", True, self.locked_color)
                    screen.blit(status_text, (skill_rect.x + 45, status_y))

        # Draw skill details at bottom if hovering
        if self.hovered_skill_id and self.hovered_skill_id in WARRIOR_SKILLS:
            self._draw_skill_details(screen, WARRIOR_SKILLS[self.hovered_skill_id])

    def _draw_skill_details(self, screen: pygame.Surface, skill):
        """
        Draw detailed description of hovered skill.

        Args:
            screen: Pygame surface to draw on
            skill: The skill to describe
        """
        details_y = self.panel_y + self.panel_height - 80
        font_desc = pygame.font.Font(None, 16)

        # Draw description (word wrap)
        words = skill.description.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font_desc.size(test_line)[0] < self.panel_width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        if current_line:
            lines.append(current_line)

        for i, line in enumerate(lines[:2]):  # Max 2 lines
            desc_text = font_desc.render(line, True, self.text_color)
            screen.blit(desc_text, (self.panel_x + 20, details_y + i * 18))

        # Draw cooldown for active skills
        if skill.skill_type == SkillType.ACTIVE:
            cooldown_text = font_desc.render(
                f"Cooldown: {skill.cooldown}s", True, config.GRAY
            )
            screen.blit(cooldown_text, (self.panel_x + 350, details_y))

    def handle_click(self, pos: tuple, warrior, right_click: bool = False) -> bool:
        """
        Handle mouse click on skills.

        Args:
            pos: Mouse position (x, y)
            warrior: The warrior entity
            right_click: If True, this is a right-click (set active)

        Returns:
            True if a skill was learned/activated, False otherwise
        """
        start_y = self.panel_y + 90
        skill_height = 60
        skill_spacing = 10

        for tier in range(1, 6):
            tier_y = start_y + (tier - 1) * (skill_height + skill_spacing)
            tier_skills = [
                (skill_id, skill)
                for skill_id, skill in WARRIOR_SKILLS.items()
                if skill.tier == tier
            ]

            skill_x = self.panel_x + 150
            skill_width = 150

            for i, (skill_id, skill) in enumerate(tier_skills):
                skill_rect = pygame.Rect(
                    skill_x + i * (skill_width + 10),
                    tier_y,
                    skill_width,
                    skill_height,
                )

                if skill_rect.collidepoint(pos):
                    if right_click:
                        # Set as active skill
                        if skill_id in warrior.skills.learned_skills:
                            if skill.skill_type == SkillType.ACTIVE:
                                warrior.skills.set_active_skill(skill_id)
                                return True
                    else:
                        # Learn skill
                        if skill_id not in warrior.skills.learned_skills:
                            # Check if can learn
                            if warrior.experience.current_level >= tier + 1:
                                if warrior.experience.get_available_skill_points() > 0:
                                    warrior.skills.learn_skill(skill_id)
                                    warrior.experience.spend_skill_point()
                                    return True

        return False
