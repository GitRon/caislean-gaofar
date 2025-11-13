"""Experience and leveling system for player progression."""


class ExperienceSystem:
    """Manages experience points and character leveling."""

    # XP required for each level (level 1 starts at 0 XP)
    XP_REQUIREMENTS = {
        1: 0,  # Start at level 1
        2: 100,  # 100 XP to reach level 2
        3: 250,  # 250 total XP to reach level 3
        4: 500,  # 500 total XP to reach level 4
        5: 1000,  # 1000 total XP to reach level 5 (max)
    }

    MAX_LEVEL = 5

    def __init__(self):
        """Initialize the experience system."""
        self.current_xp = 0
        self.current_level = 1
        self.skill_points = 0
        self.spent_skill_points = 0

    def add_xp(self, amount: int) -> bool:
        """
        Add experience points and check for level up.

        Args:
            amount: Amount of XP to add

        Returns:
            True if leveled up, False otherwise
        """
        if self.current_level >= self.MAX_LEVEL:
            # Already at max level
            return False

        self.current_xp += amount
        leveled_up = False

        # Check for level ups (can level up multiple times)
        while self.current_level < self.MAX_LEVEL:
            next_level = self.current_level + 1
            xp_needed = self.XP_REQUIREMENTS[next_level]

            if self.current_xp >= xp_needed:
                self.current_level = next_level
                self.skill_points += 1  # Award 1 skill point per level
                leveled_up = True
            else:
                break

        return leveled_up

    def get_xp_for_next_level(self) -> int:
        """
        Get XP required for next level.

        Returns:
            XP needed for next level, or 0 if at max level
        """
        if self.current_level >= self.MAX_LEVEL:
            return 0
        return self.XP_REQUIREMENTS[self.current_level + 1]

    def get_xp_progress(self) -> float:
        """
        Get progress toward next level as a percentage.

        Returns:
            Progress from 0.0 to 1.0, or 1.0 if at max level
        """
        if self.current_level >= self.MAX_LEVEL:
            return 1.0

        current_level_xp = self.XP_REQUIREMENTS[self.current_level]
        next_level_xp = self.XP_REQUIREMENTS[self.current_level + 1]
        xp_in_level = self.current_xp - current_level_xp
        xp_needed_for_level = next_level_xp - current_level_xp

        return xp_in_level / xp_needed_for_level if xp_needed_for_level > 0 else 1.0

    def get_available_skill_points(self) -> int:
        """
        Get number of unspent skill points.

        Returns:
            Number of skill points available to spend
        """
        return self.skill_points - self.spent_skill_points

    def spend_skill_point(self) -> bool:
        """
        Spend a skill point.

        Returns:
            True if successful, False if no points available
        """
        if self.get_available_skill_points() > 0:
            self.spent_skill_points += 1
            return True
        return False

    def get_current_level(self) -> int:
        """Get current character level."""
        return self.current_level

    def get_current_xp(self) -> int:
        """Get current experience points."""
        return self.current_xp

    def is_max_level(self) -> bool:
        """Check if at maximum level."""
        return self.current_level >= self.MAX_LEVEL
