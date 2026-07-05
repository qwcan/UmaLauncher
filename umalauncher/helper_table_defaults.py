from enum import Enum
import copy
import helper_table_elements as hte
import util
import settings_elements as se
import constants
from loguru import logger

def compensate_overcap(game_state, command):
    # Compensate for overcapped stats by doubling any gained stats that bring the current stats over 1200.
    current_stats = {command_type: game_state[command_type]['current_stats'] for command_type in game_state}
    gained_stats = copy.deepcopy(command['gained_stats'])
    for stat in current_stats:
        if current_stats[stat] + gained_stats[stat] > 1200:
            stats_until_1200 = max(1200 - current_stats[stat], 0)
            gained_stats[stat] = stats_until_1200 + (gained_stats[stat] - stats_until_1200) * 2

    return gained_stats


class CurrentStatsRow(hte.Row):
    long_name = "Current stats"
    short_name = "Current Stats"
    description = "Shows the current stats of each facility."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            gained_stats = command['current_stats']
            cells.append(hte.Cell(gained_stats))

        return cells


class GainedStatsSettings(se.NewSettings):
    _settings = {
        "enable_skillpts": se.Setting(
            "Include skill points",
            "Include skill points in the total.",
            False,
            se.SettingType.BOOL,
        ),
        "displayed_value": se.Setting(
            "Displayed value(s)",
            "Which value(s) to display.",
            0,
            se.SettingType.COMBOBOX,
            choices=["Raw gained stats", "Overcap-compensated gained stats", "Both"],
        ),
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most gained stats.",
            True,
            se.SettingType.BOOL,
        ),
        "highlight_max_overcapped": se.Setting(
            "Highlight max (compensated)",
            "(Only when 'highlight max' is enabled and both stats types are displayed.)\nHighlights the facility with the most gained stats, using the compensated values.",
            True,
            se.SettingType.BOOL,
        ),
        "highlight_color": se.Setting(
            "Highlight color",
            "The color to use for highlighting.",
            "#90EE90",
            se.SettingType.COLOR,
        ),
    }

def make_gained_stats_text(gained_stats, gained_stats_compensated, highlight_color="#90EE90", highlight=0):
    stats_highlight_span_open = f"<span style=\"font-weight: bold; color: {highlight_color};\">"
    stats_highlight_span_close = "</span>"

    if gained_stats_compensated == gained_stats:
        if highlight < 1:
            return f"{gained_stats}"
        else:
            return f"{stats_highlight_span_open}{gained_stats}{stats_highlight_span_close}"
    else:
        if highlight == 1:
            return f"{stats_highlight_span_open}{gained_stats}{stats_highlight_span_close} ({gained_stats_compensated})"
        elif highlight == 2:
            return f"{gained_stats} ({stats_highlight_span_open}{gained_stats_compensated}{stats_highlight_span_close})"
        else:
            return f"{gained_stats} ({gained_stats_compensated})"

class GainedStatsRow(hte.Row):
    long_name = "Stats gained total"
    short_name = "Stat Gain"
    description = "Shows the total stats gained per facility. This includes stats gained outside the facility itself. \nExcludes skill points by default."

    def __init__(self):
        super().__init__()
        self.settings = GainedStatsSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        all_gained_stats = []
        all_gained_stats_compensated = []
        for command in game_state.values():
            gained_stats = sum(command['gained_stats'].values())
            gained_stats_compensated = sum(compensate_overcap(game_state, command).values())
            if self.settings.enable_skillpts.value:
                gained_stats += command['gained_skillpt']
                gained_stats_compensated += command['gained_skillpt']
            all_gained_stats.append(gained_stats)
            all_gained_stats_compensated.append(gained_stats_compensated)

        if self.settings.highlight_max_overcapped.value and self.settings.displayed_value.value == 2 or self.settings.displayed_value.value == 1:
            max_gained_stats = max(all_gained_stats_compensated)
        else:
            max_gained_stats = max(all_gained_stats)

        for i, gained_stats in enumerate(all_gained_stats):
            gained_stats_compensated = all_gained_stats_compensated[i]
            if self.settings.highlight_max.value:
                if self.settings.displayed_value.value == 2:
                    if self.settings.highlight_max_overcapped.value and gained_stats_compensated == max_gained_stats:
                        cells.append(hte.Cell(make_gained_stats_text(gained_stats, gained_stats_compensated, self.settings.highlight_color.value, highlight=2)))
                        continue
                    elif not self.settings.highlight_max_overcapped.value and gained_stats == max_gained_stats:
                        cells.append(hte.Cell(make_gained_stats_text(gained_stats, gained_stats_compensated, self.settings.highlight_color.value, highlight=1)))
                        continue
                elif self.settings.displayed_value.value == 0 and gained_stats == max_gained_stats:
                    cells.append(hte.Cell(gained_stats, bold=True, color=self.settings.highlight_color.value))
                    continue
                elif self.settings.displayed_value.value == 1 and gained_stats_compensated == max_gained_stats:
                    cells.append(hte.Cell(gained_stats_compensated, bold=True, color=self.settings.highlight_color.value))
                    continue

            if self.settings.displayed_value.value == 2:
                cells.append(hte.Cell(make_gained_stats_text(gained_stats, gained_stats_compensated)))
            elif self.settings.displayed_value.value == 0:
                cells.append(hte.Cell(gained_stats))
            elif self.settings.displayed_value.value == 1:
                cells.append(hte.Cell(gained_stats_compensated))

        return cells

class GainedStatsDistributionSettings(se.NewSettings):
    _settings = {
        "include_skillpts": se.Setting(
            "Include skill points",
            "Include skill points in the row.",
            False,
            se.SettingType.BOOL
        ),
        "displayed_value": se.Setting(
            "Displayed value(s)",
            "Which value(s) to display.",
            0,
            se.SettingType.COMBOBOX,
            choices=["Raw gained stats", "Overcap-compensated gained stats", "Both"]
        ),
    }


class GainedStatsDistributionRow(hte.Row):
    long_name = "Stats gained distribution"
    short_name = "Stat Gain <br>Distribution"
    description = "Shows the stats gained per facility per type. This includes stats gained outside the facility itself."

    def __init__(self):
        super().__init__()
        self.settings = GainedStatsDistributionSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            gained_stats = command['gained_stats']
            gained_stats_compensated = compensate_overcap(game_state, command)

            def display_value(gained, compensated):
                if self.settings.displayed_value.value == 0:
                    return gained
                elif self.settings.displayed_value.value == 1:
                    return compensated
                elif self.settings.displayed_value.value == 2:
                    return make_gained_stats_text(gained, compensated)

            out_lines = []
            if gained_stats['speed'] > 0:
                out_lines.append(f"Spd: {display_value(gained_stats['speed'], gained_stats_compensated['speed'])}")
            if gained_stats['stamina'] > 0:
                out_lines.append(f"Sta: {display_value(gained_stats['stamina'], gained_stats_compensated['stamina'])}")
            if gained_stats['power'] > 0:
                out_lines.append(f"Pow: {display_value(gained_stats['power'], gained_stats_compensated['power'])}")
            if gained_stats['guts'] > 0:
                out_lines.append(f"Gut: {display_value(gained_stats['guts'], gained_stats_compensated['guts'])}")
            if gained_stats['wiz'] > 0:
                out_lines.append(f"Wis: {display_value(gained_stats['wiz'], gained_stats_compensated['wiz'])}")

            if self.settings.include_skillpts.value and command['gained_skillpt'] > 0:
                out_lines.append(f"Skl: {command['gained_skillpt']}")
            
            cells.append(hte.Cell('<br>'.join(out_lines)))

        return cells


class GainedEnergySettings(se.NewSettings):
    _settings = {
        "enable_colors": se.Setting(
            "Enable colors",
            "Enables coloring of the energy gained or lost.",
            False,
            se.SettingType.BOOL,
        ),
        "gain_color": se.Setting(
            "Energy gain color",
            "The color to use for energy gained.",
            "#90EE90",
            se.SettingType.COLOR
        ),
        "loss_color": se.Setting(
            "Energy loss color",
            "The color to use for energy lost.",
            "#FFA500",
            se.SettingType.COLOR
        ),
    }

class GainedEnergyRow(hte.Row):
    long_name = "Energy gained/lost"
    short_name = "Energy"
    description = "Shows the total energy gained or lost per facility."

    def __init__(self):
        super().__init__()
        self.settings = GainedEnergySettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            gained_energy = command['gained_energy']
            if self.settings.enable_colors.value:
                if gained_energy > 0:
                    cells.append(hte.Cell(gained_energy, bold=True, color=self.settings.gain_color.value))
                elif gained_energy < 0:
                    cells.append(hte.Cell(gained_energy, bold=True, color=self.settings.loss_color.value))
                else:
                    cells.append(hte.Cell(gained_energy))
            else:
                cells.append(hte.Cell(gained_energy))

        return cells


class TotalBondSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most total bond.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use for highlighting the facility with the most total bond.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class TotalBondRow(hte.Row):
    long_name = "Bond gained total"
    short_name = "Total Bond"
    description = "Shows the total bond gain for each facility. Total includes all bond gains of all supports and Akikawa, until the bar is filled."

    def __init__(self):
        super().__init__()
        self.settings = TotalBondSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        max_total_bond = max(facility['total_bond'] for facility in game_state.values())

        for command in game_state.values():
            total_bond = command['total_bond']
            if self.settings.highlight_max.value and max_total_bond > 0 and total_bond == max_total_bond:
                cells.append(hte.Cell(total_bond, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(total_bond))

        return cells


class UsefulBondSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most useful bond.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use for highlighting the facility with the most useful bond.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }



class UsefulBondRow(hte.Row):
    long_name = "Useful bond gained total"
    short_name = "Useful Bond"
    description = "Shows the useful bond gain for each facility. Useful includes supports until orange bar, excluding friend/group cards.<br>Also Akikawa until green bar (except Project L'Arc). During L'Arc, Mei counts as useful until green bar."

    def __init__(self):
        super().__init__()
        self.settings = UsefulBondSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        max_useful_bond = max(facility['useful_bond'] for facility in game_state.values())

        for command in game_state.values():
            useful_bond = command['useful_bond']
            if self.settings.highlight_max.value and max_useful_bond > 0 and useful_bond == max_useful_bond:
                cells.append(hte.Cell(useful_bond, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(useful_bond))

        return cells


class GainedSkillptSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most gained skill points.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use for highlighting the facility with the most gained skill points.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class GainedSkillptRow(hte.Row):
    long_name = "Skill points gained"
    short_name = "Skill Points"
    description = "Shows the total skill points gained per facility."

    def __init__(self):
        super().__init__()
        self.settings = GainedSkillptSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        max_gained_skillpt = max(facility['gained_skillpt'] for facility in game_state.values())

        for command in game_state.values():
            gained_skillpt = command['gained_skillpt']
            if self.settings.highlight_max.value and max_gained_skillpt > 0 and gained_skillpt == max_gained_skillpt:
                cells.append(hte.Cell(gained_skillpt, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(gained_skillpt))

        return cells


class FailPercentageSettings(se.NewSettings):
    _settings = {
        "enable_colors": se.Setting(
            "Enable colors",
            "Enables coloring of the fail percentage.",
            True,
            se.SettingType.BOOL,
        ),
        "warning_color": se.Setting(
            "Warning color",
            "The color to use for the fail percentage when it is above the warning threshold.",
            "#FFA500",
            se.SettingType.COLOR,
        ),
        "warning_threshold": se.Setting(
            "Warning threshold",
            "The number from which the fail percentage uses the warning color.",
            1,
            se.SettingType.INT,
            min_value=0,
            max_value=100
        ),
        "alert_color": se.Setting(
            "Alert color",
            "The color to use for the fail percentage when it is above the alert threshold.",
            "#FF0000",
            se.SettingType.COLOR,
        ),
        "alert_threshold": se.Setting(
            "Alert threshold",
            "The number from which the fail percentage uses the alert color.",
            30,
            se.SettingType.INT,
            min_value=0,
            max_value=100
        ),
    }

class FailPercentageRow(hte.Row):
    long_name = "Fail percentage"
    short_name = "Fail %"
    description = "Shows the fail percentage per facility."

    def __init__(self):
        super().__init__()
        self.settings = FailPercentageSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            fail_percentage = command['failure_rate']
            fail_string = f"{fail_percentage}%"
            if not self.settings.enable_colors.value or fail_percentage == 0:
                cells.append(hte.Cell(fail_string))
                continue

            if fail_percentage >= self.settings.alert_threshold.value:
                cells.append(hte.Cell(fail_string, color=self.settings.alert_color.value, bold=True))
            elif fail_percentage >= self.settings.warning_threshold.value:
                cells.append(hte.Cell(fail_string, color=self.settings.warning_color.value, bold=True))
            else:
                cells.append(hte.Cell(fail_string))
                

        return cells


class LevelRow(hte.Row):
    long_name = "Facility level"
    short_name = "Level"
    description = "Shows the level of each facility."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            cells.append(hte.Cell(command['level']))

        return cells

class GrandMastersFragmentsSettings(se.NewSettings):
    _settings = {
        "double_color": se.Setting(
            "Double fragment color",
            "The color to use to indicate a double fragment.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class GrandMastersFragmentsRow(hte.Row):
    long_name = "Grand Masters fragments"
    short_name = "Fragments"
    description = "[Scenario-specific] Shows the total Grand Masters fragments on each facility. Hidden in other scenarios."

    def __init__(self):
        super().__init__()
        self.settings = GrandMastersFragmentsSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 5:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            fragment_id = command['gm_fragment']
            is_double = bool(command['gm_fragment_double'])

            cell_text = f"<div style=\"display: flex; align-items: center; justify-content: center;\"><img src=\"{util.get_gm_fragment_dict()[fragment_id]}\" height=\"30\" width=\"28\" />"

            if is_double:
                cell_text += "<div>x2</div>"
            
            cell_text += "</div>"

            cells.append(hte.Cell(cell_text, bold=True, color=self.settings.double_color.value))

        return cells
    
    def to_tr(self, command_info):
        if command_info['speed']['scenario_id'] != 5:
            return ""

        return super().to_tr(command_info)


class GrandLiveTotalTokensSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most Grand Live tokens.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most Grand Live tokens.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class GrandLiveTotalTokensRow(hte.Row):
    long_name = "Grand Live tokens total"
    short_name = "Token Gain"
    description = "[Scenario-specific] Shows the total Grand Live tokens on each facility. Hidden in other scenarios."

    def __init__(self):
        super().__init__()
        self.settings = GrandLiveTotalTokensSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 3:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        max_gl_tokens = max(sum(command['gl_tokens'].values()) for command in game_state.values())

        for command in game_state.values():
            gl_tokens = sum(command['gl_tokens'].values())
            if self.settings.highlight_max.value and max_gl_tokens > 0 and gl_tokens == max_gl_tokens:
                cells.append(hte.Cell(gl_tokens, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(gl_tokens))

        return cells



class GrandLiveTokensDistributionRow(hte.Row):
    long_name = "Grand Live tokens gained distribution"
    short_name = "Token Gain <br>Distribution"
    description = "[Scenario-specific] Shows the distribution of Grand Live tokens on each facility. Hidden in other scenarios."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 3:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            gl_tokens_dict = command['gl_tokens']
            
            cell_text = f"<div style=\"display: flex; align-items: center; justify-content: center; gap: 0.2rem;\">"
            for token_type, value in gl_tokens_dict.items():
                if value <= 0:
                    continue
                cell_text += f"<div style=\"display: flex; flex-direction: column; align-items: center; justify-content: center;\"><img src=\"{util.get_gl_token_dict()[token_type]}\" height=\"24\" width=\"24\" />"
                cell_text += f"<div>{value}</div>"
                cell_text += "</div>"

            cell_text += "</div>"

            cells.append(hte.Cell(cell_text))

        return cells
    
    def to_tr(self, command_info):
        if list(command_info.values())[0]['scenario_id'] != 3:
            return ""

        return super().to_tr(command_info)
    

class RainbowCountRow(hte.Row):
    long_name = "Rainbow count"
    short_name = "Rainbows"
    description = "Shows the total number of rainbows on each facility."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            cells.append(hte.Cell(command['rainbow_count']))

        return cells


class PartnerCountSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most training partners.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most training partners.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class PartnerCountRow(hte.Row):
    long_name = "Training partner count"
    short_name = "Partners"
    description = "Shows the total number of training partners on each facility. This includes partners that don't give extra stats when training together."

    def __init__(self):
        super().__init__()
        self.settings = PartnerCountSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        highest_partner_count = max(command['partner_count'] for command in game_state.values())

        for command in game_state.values():
            if self.settings.highlight_max.value and highest_partner_count > 0 and command['partner_count'] == highest_partner_count:
                cells.append(hte.Cell(command['partner_count'], bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(command['partner_count']))

        return cells


class UsefulPartnerCountSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most useful training partners.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most useful training partners.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class UsefulPartnerCountRow(hte.Row):
    long_name = "Useful training partner count"
    short_name = "Useful<br>Partners"
    description = "Shows the number of useful training partners on each facility. Useful partners are any that give extra stats when training together."

    def __init__(self):
        super().__init__()
        self.settings = UsefulPartnerCountSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        highest_useful_partner_count = max(command['useful_partner_count'] for command in game_state.values())

        for command in game_state.values():
            if self.settings.highlight_max.value and highest_useful_partner_count > 0 and command['useful_partner_count'] == highest_useful_partner_count:
                cells.append(hte.Cell(command['useful_partner_count'], bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(command['useful_partner_count']))

        return cells


class HintCountSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most skill hints available.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most skill hints available.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class HintCountRow(hte.Row):
    long_name = "Skill hint count"
    short_name = "Skill Hints"
    description = "Shows the total number of skill hints available at each facility."

    def __init__(self):
        super().__init__()
        self.settings = HintCountSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        cells = [hte.Cell(self.short_name, title=self.description)]

        highest_hint_count = max(command['num_hints'] for command in game_state.values())

        for command in game_state.values():
            if self.settings.highlight_max.value and highest_hint_count > 0 and command['num_hints'] == highest_hint_count:
                cells.append(hte.Cell(command['num_hints'], bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(command['num_hints']))

        return cells


class UnityTrainingCountSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most Unity Training partners.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most Unity Training partners.",
            "#90EE90",
            se.SettingType.COLOR
        ),
        "highlight_burst_color": se.Setting(
            "Highlight burst color",
            "The color to use to highlight facilities with a Spirit Burst Unity Training partner(s).",
            "#1777E0",
            se.SettingType.COLOR
        ),
        "highlight_max_burst_color": se.Setting(
            "Highlight max burst color",
            "The color to use to highlight the facility with the most Spirit Burst Unity Training partner(s).",
            "#0070FF",
            se.SettingType.COLOR
        ),
    }

class UsefulUnityTrainingCountSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most useful Unity Training partners.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most useful Unity Training partners.",
            "#90EE90",
            se.SettingType.COLOR
        ),
        "highlight_burst_color": se.Setting(
            "Highlight burst color",
            "The color to use to highlight facilities with a Spirit Burst Unity Training partner(s).",
            "#1777E0",
            se.SettingType.COLOR
        ),
        "highlight_max_burst_color": se.Setting(
            "Highlight max burst color",
            "The color to use to highlight the facility with the most Spirit Burst Unity Training partner(s).",
            "#0070FF",
            se.SettingType.COLOR
        ),
    }

class UnityScoreSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most Unity Score.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most Unity Score.",
            "#90EE90",
            se.SettingType.COLOR
        )
    }

class UnityTrainingCountRow(hte.Row):
    long_name = "Unity Training partner count"
    short_name = "Unity"
    description = "[Scenario-specific] Shows the number of Unity Training partners on each facility."

    def __init__(self):
        super().__init__()
        self.settings = UnityTrainingCountSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 2:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]


        highest_unity_partner_count = max(command['unity_partner_count'] for command in game_state.values())
        highest_spirit_burst_partner_count = max(command['spirit_burst_partner_count'] for command in game_state.values())

        for command in game_state.values():
            bold = False
            color = None
            # Max highlight overrides default
            if self.settings.highlight_max.value and highest_unity_partner_count > 0 and command['unity_partner_count'] == highest_unity_partner_count:
                bold = True
                color = self.settings.highlight_max_color.value
            # spirit burst overrides highlight
            if command['spirit_burst_partner_count'] > 0:
                bold = True
                color = self.settings.highlight_burst_color.value
            # max spirit burst overrides spirit burst
            if self.settings.highlight_max.value and highest_spirit_burst_partner_count > 0 and command['spirit_burst_partner_count'] == highest_spirit_burst_partner_count:
                bold = True
                color = self.settings.highlight_max_burst_color.value
            cells.append(hte.Cell(command['unity_partner_count'], bold=bold, color=color))

        return cells

class UsefulUnityTrainingCountRow(hte.Row):
    long_name = "Useful Unity Training partner count"
    short_name = "Useful Unity"
    description = "[Scenario-specific] Shows the number of useful Unity Training partners on each facility. Useful Unity Training partners are any that haven't already had a Spirit Burst."

    def __init__(self):
        super().__init__()
        self.settings = UsefulUnityTrainingCountSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 2:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]


        highest_unity_partner_count = max(command['useful_unity_partner_count'] for command in game_state.values())
        highest_spirit_burst_partner_count = max(command['spirit_burst_partner_count'] for command in game_state.values())

        for command in game_state.values():
            bold = False
            color = None
            # Max highlight overrides default
            if self.settings.highlight_max.value and highest_unity_partner_count > 0 and command['useful_unity_partner_count'] == highest_unity_partner_count:
                bold = True
                color = self.settings.highlight_max_color.value
            # spirit burst overrides highlight
            if command['spirit_burst_partner_count'] > 0:
                bold = True
                color = self.settings.highlight_burst_color.value
            # max spirit burst overrides spirit burst
            if self.settings.highlight_max.value and highest_spirit_burst_partner_count > 0 and command['spirit_burst_partner_count'] == highest_spirit_burst_partner_count:
                bold = True
                color = self.settings.highlight_max_burst_color.value
            cells.append(hte.Cell(command['useful_unity_partner_count'], bold=bold, color=color))

        return cells

class UnityScoreRow(hte.Row):
    long_name = "Unity Score"
    short_name = "Unity Score"
    description = "[Scenario-specific] Shows calculated Unity training score on each facility."

    def __init__(self):
        super().__init__()
        self.settings = UnityScoreSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 2:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        def calc_unity_score(command, training) -> float:
            current_turn = command['turn']
            wiz_count = 1 if training == "wiz" else 0
            score = 0.0

            if current_turn < 36:
                score = 2.0 * command['useful_unity_partner_count'] + command['useful_bond'] / 7.0 + command['riko_count'] + command['unity_near_explode_partner_count'] + wiz_count + command['rainbow_count'] + 8.0 * command['spirit_burst_partner_count']
            elif current_turn < 48:
                score = 2.0 * command['useful_unity_partner_count'] + 2.0 * command['useful_bond'] / 7.0 + command['riko_count'] + command['unity_near_explode_partner_count'] + wiz_count + command['rainbow_count'] + 8.0 * command['spirit_burst_partner_count']
            elif current_turn < 60:
                score = 2.0 * command['useful_unity_partner_count'] + 2.0 * command['useful_bond'] / 7.0 + command['riko_count'] + command['unity_near_explode_partner_count'] + 2.0 * command['rainbow_count'] + 2.0 * command['spirit_burst_partner_count']
            else:
                score = 2.0 * command['useful_unity_partner_count'] + 2.0 * command['useful_bond'] / 7.0 + command['riko_count'] + command['unity_near_explode_partner_count'] + 2.0 * command['rainbow_count'] + command['spirit_burst_partner_count']
            return round(score, 2)

        highest_unity_score_count = max(calc_unity_score(command, key) for key, command in game_state.items())

        for key, command in game_state.items():
            bold = False
            color = None
            local_score = calc_unity_score(command, key)
            # Max highlight overrides default
            if self.settings.highlight_max.value and highest_unity_score_count > 0 and local_score == highest_unity_score_count:
                bold = True
                color = self.settings.highlight_max_color.value

            cells.append(hte.Cell(local_score, bold=bold, color=color))

        return cells

class LArcStarGaugeGainSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most star gauge gain.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most star gauge gain.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class LArcStarGaugeGainRow(hte.Row):
    long_name = "L'Arc star gauge gain"
    short_name = "Star Gauge"
    description = "[Scenario-specific] Shows the total L'Arc star gauge gain per facility. Hidden in other scenarios."

    def __init__(self):
        super().__init__()
        self.settings = LArcStarGaugeGainSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 6:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        max_star_gauge_gain = max(facility['arc_gauge_gain'] for facility in game_state.values())

        for command in game_state.values():
            star_gauge_gain = command['arc_gauge_gain']
            if self.settings.highlight_max.value and max_star_gauge_gain > 0 and star_gauge_gain == max_star_gauge_gain:
                cells.append(hte.Cell(star_gauge_gain, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(star_gauge_gain))

        return cells


class LArcAptitudePointsSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most aptitude points gained.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most aptitude points gained.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class LArcAptitudePointsRow(hte.Row):
    long_name = "L'Arc aptitude points gained"
    short_name = "Aptitude<br>Points"
    description = "[Scenario-specific] Shows the total L'Arc aptitude points gained per facility. Hidden in other scenarios."

    def __init__(self):
        super().__init__()
        self.settings = LArcAptitudePointsSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 6:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        max_aptitude_gain = max(facility['arc_aptitude_gain'] for facility in game_state.values())

        for command in game_state.values():
            aptitude_gain = command['arc_aptitude_gain']
            if self.settings.highlight_max.value and max_aptitude_gain > 0 and aptitude_gain == max_aptitude_gain:
                cells.append(hte.Cell(aptitude_gain, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(aptitude_gain))

        return cells


class UAFSportPointGainRow(hte.Row):
    long_name = "UAF Sports point gain"
    short_name = "Sport Gain"
    description = "[Scenario-specific] Displays the points that each genre will gain."

    def __init__(self):
        super().__init__()
        self.settings = UAFSportPointGainSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 7:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]
        
        uaf_sport_gains = {}
        for command in game_state.values():
            for command_id, gain in command['uaf_sport_gain'].items():
                group = (command_id // 100) % 10
                uaf_sport_gains[group] = uaf_sport_gains.get(group, 0) + gain
        
        # Find the sport group with the highest total gain
        max_gain = max(uaf_sport_gains.values())

        # Identify all groups with the maximum total gain
        max_gain_groups = [group for group, gain in uaf_sport_gains.items() if gain == max_gain]

        # Highlight sports in groups with the maximum total gain
        uaf_sport_gain = command['uaf_sport_gain']
        for command_id, gain in uaf_sport_gain.items():
            group = (command_id // 100) % 10
            if self.settings.highlight_max.value and group in max_gain_groups and uaf_sport_gains[group] > 0:
                cells.append(hte.Cell(gain, bold=True, color=self.settings.highlight_max_color.value, background=constants.UAF_COLOR_DICT[str(command_id)[1]]))
            else:
                cells.append(hte.Cell(gain, background=constants.UAF_COLOR_DICT[str(command_id)[1]]))

        return cells

class UAFSportPointGainSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most aptitude points gained.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most aptitude points gained.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class EnergyRatio(hte.Row):
    long_name = "Energy to Stat Ratio"
    short_name = "Energy Ratio"
    description = "Displays the ratio of Energy Spend compared to a specific stat."

    def __init__(self):
        super().__init__()
        self.settings = EnergyRatioSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:

        cells = [hte.Cell(self.short_name, title=self.description)]
        
        max_gain = 0
        ratio_list = []
        for command in game_state.values():
            energy = command['gained_energy']
            chosen_commands = command['gained_stats']
        
            if self.settings.comparison_choice.value == 0:
                chosen_commands = sum(command['gained_stats'].values())
            elif self.settings.comparison_choice.value == 1:
                chosen_commands = command['useful_bond']
            elif self.settings.comparison_choice.value == 2:
                chosen_commands = command['total_bond']
            elif self.settings.comparison_choice.value == 3:
                chosen_commands = command['gained_skillpt']
            
            if energy >= 0:
                ratio_list.append(-1)
                continue
            
            current_ratio = round(chosen_commands / abs(energy), 2)
            ratio_list.append(current_ratio)
            
            if current_ratio > max_gain:
                max_gain = current_ratio
                
        for ratio in ratio_list: 
            display_text = ""
            
            if ratio != -1:
                display_text = ratio
            
            if ratio == max_gain:
                cells.append(hte.Cell(display_text, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(display_text))
                
        return cells


class EnergyRatioSettings(se.NewSettings):
    _settings = {
        "comparison_choice": se.Setting(
            "Comparison",
            "Value to calculate the Ratio for.",
            0,
            se.SettingType.COMBOBOX,
            choices=["Stats Gained", "Useful Bond", "Total Bond", "Gained Skillpt"],
        ),
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the highest Ratio.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the highest Ratio.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class GFFVegetablesSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the most vegetables planted.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the most vegetables planted.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class DYISettings(se.NewSettings):

    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the greatest point gain.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the greatest point gain.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }

class OnsenSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the greatest point gain.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the greatest point gain.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class DreamPointsSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the greatest DP gain.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the greatest DP gain.",
            "#90EE90",
            se.SettingType.COLOR
        ),
        "hide_row_if_no_gain": se.Setting(
            "Hide row if no DP gain",
            "Hide this row if no DP can be gained from any training facilities.",
            False,
            se.SettingType.BOOL
        ),
    }


class GFFVegetablesRow(hte.Row):
    long_name = "GFF Vegetable Gain"
    short_name = "Veggies"
    description = "[Scenario-specific] Displays the number of vegetables planted for each training facility."

    def __init__(self):
        super().__init__()
        self.settings = GFFVegetablesSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 8:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        harvest_sums = {}

        for command_key, command_data in game_state.items():
            harvest_sum = 0
            if 'material_harvest_info_array' in command_data:
                harvest_sum = sum([data['harvest_num'] for data in command_data['material_harvest_info_array']])
            harvest_sums[command_key] = harvest_sum
        
        max_harvest = max(harvest_sums.values())

        for command_key, harvest in harvest_sums.items():
            if self.settings.highlight_max.value and harvest == max_harvest and max_harvest > 0:
                cells.append(hte.Cell(harvest, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(harvest))
        
        return cells


class GFFVegetablesDistributionRow(hte.Row):
    long_name = "GFF Vegetables Distribution"
    short_name = "Veggies <br>Distribution"
    description = "[Scenario-specific] Displays the distribution of vegetables planted for each training facility."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 8:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]


        for command in game_state.values():
            harvest_info = command.get('material_harvest_info_array', [])

            text = ""

            for veg_data in harvest_info:
                img = veg_data['img']
                count = veg_data['harvest_num']
                if count <= 0:
                    continue
                text += f"""<div style="display: flex; align-items: center; justify-content: center; gap: 0.2rem;"><img src="{util.get_gff_veg_image_dict()[img]}" height="16" width="16" style="height:16px;width:auto;" />{count}</div>"""

            cells.append(hte.Cell(text))
        
        return cells


class RMUTotalResearchLevelSettings(se.NewSettings):
    _settings = {
        "highlight_max": se.Setting(
            "Highlight max",
            "Highlights the facility with the highest research level gain.",
            True,
            se.SettingType.BOOL
        ),
        "highlight_max_color": se.Setting(
            "Highlight max color",
            "The color to use to highlight the facility with the highest research level gain.",
            "#90EE90",
            se.SettingType.COLOR
        ),
    }


class RMUTotalResearchLevelRow(hte.Row):
    long_name = "Run! Mecha Umamusume research level total"
    short_name = "Research Gain"
    description = "[Scenario-specific] Shows the total research level gained on each facility. Hidden in other scenarios."

    def __init__(self):
        super().__init__()
        self.settings = RMUTotalResearchLevelSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 9:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        max_research_lvl = max(sum([data['value'] for data in command['point_up_info_array']]) for command in game_state.values())

        for command in game_state.values():
            research_lvl = sum([data['value'] for data in command['point_up_info_array']])
            if self.settings.highlight_max.value and max_research_lvl > 0 and research_lvl == max_research_lvl:
                cells.append(hte.Cell(research_lvl, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(research_lvl))

        return cells


class RMUResearchDistributionRow(hte.Row):
    long_name = "Run! Mecha Umamusume research level distribution"
    short_name = "Research Lvl <br>Distribution"
    description = "[Scenario-specific] Shows the distribution of research level gained on each facility. Hidden in other scenarios."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 9:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        for command in game_state.values():
            research_list = command['point_up_info_array']
            research_list = sorted(research_list, key=lambda x: constants.RMU_KEY_TO_ORDER[x['status_type']])
            
            cell_text = f"<div style=\"display: flex; align-items: center; justify-content: center; gap: 0.2rem;\">"
            for data_dict in research_list:
                value = data_dict['value']
                id = data_dict['status_type']
                if value <= 0:
                    continue
                cell_text += f"<div style=\"display: flex; flex-direction: column; align-items: center; justify-content: center;\"><img src=\"{util.get_rmu_image_dict()[str(id)]}\" height=\"29\" width=\"24\" style=\"margin-bottom: -2px\" />"
                cell_text += f"<div>{value}</div>"
                cell_text += "</div>"

            cell_text += "</div>"

            cells.append(hte.Cell(cell_text))

        return cells
    
    def to_tr(self, command_info):
        if list(command_info.values())[0]['scenario_id'] != 9:
            return ""

        return super().to_tr(command_info)

class DYIPointsDistributionRow(hte.Row):
    long_name = "Design Your Island points distribution"
    short_name = "Points <br>Distribution"
    description = "[Scenario-specific] Shows the distribution of points gained on each facility. Hidden in other scenarios."


    def __init__(self):
        super().__init__()
        self.settings = DYISettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 11:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        point_sums = {}

        for command_key, command_data in game_state.items():
            point_sum = 0
            #logger.info( f"Command key: {command_key}")
            #logger.info( f"Command data: {command_data}")
            if 'pioneer_point_gain_info_array' in command_data:
                #logger.info( f"Command data: {command_data['pioneer_point_gain_info_array']}")
                point_sum = command_data['pioneer_point_gain_info_array']
            point_sums[command_key] = point_sum

        max_points = max(point_sums.values())

        for command_key, points in point_sums.items():
            if self.settings.highlight_max.value and points == max_points and max_points > 0:
                cells.append(hte.Cell(points, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(points))

        return cells

    def to_tr(self, command_info):
        if list(command_info.values())[0]['scenario_id'] != 11:
            return ""

        return super().to_tr(command_info)


class OnsenPointsDistributionRow(hte.Row):
    long_name = "Yukoma Hot Springs points distribution"
    short_name = "Points <br>Distribution"
    description = "[Scenario-specific] Shows the distribution of points gained on each facility. Hidden in other scenarios."


    def __init__(self):
        super().__init__()
        self.settings = OnsenSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 12:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        point_sums = {}

        for command_key, command_data in game_state.items():
            point_sum = 0
            if 'onsen_points_gain' in command_data :
                point_sum = command_data['onsen_points_gain']
            point_sums[command_key] = point_sum

        max_points = max(point_sums.values())

        for command_key, points in point_sums.items():
            if self.settings.highlight_max.value and points == max_points and max_points > 0:
                cells.append(hte.Cell(points, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(points))

        return cells

    def to_tr(self, command_info):
        if list(command_info.values())[0]['scenario_id'] != 12:
            return ""

        return super().to_tr(command_info)


class DreamPointsRow(hte.Row):
    long_name = "Beyond Dreams DP gain"
    short_name = "DP Gain"
    description = "[Scenario-specific] Displays the number of Dream Points gained for each training facility."


    def __init__(self):
        super().__init__()
        self.settings = DreamPointsSettings()

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 13:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]

        has_ssr_casino_drive = list(game_state.values())[0]['has_ssr_casino_drive']
        dp_sums = {}
        for command_key, command_data in game_state.items():
            point_sum = 0
            for member in command_data['team_member_info_array']:
                point_sum += (2 if has_ssr_casino_drive else 1) if member['gain_exp'] == 0 else 0
            dp_sums[command_key] = point_sum
        max_points = max(dp_sums.values())
        if list(game_state.values())[0]['turn'] > 60:
            return [] # Can't gain DP after the last Reflection/Strategy Meeting
        if max_points == 0 and self.settings.hide_row_if_no_gain.value:
            return [] # Don't show row if no DP gain

        for command_key, command_data in game_state.items():
            cell_text = f"{dp_sums[command_key]}"
            if dp_sums[command_key] != 0 and dp_sums[command_key] == max_points and self.settings.highlight_max.value:
                cells.append(hte.Cell(cell_text, bold=True, color=self.settings.highlight_max_color.value))
            else:
                cells.append(hte.Cell(cell_text))

        return cells

class RamenExpertiseSettings(se.NewSettings):
    _settings = {
        "highlight_level_up": se.Setting(
            "Highlight Expertise Level Up",
            "Highlights the facilities that will level up a ramen expertise",
            True,
            se.SettingType.BOOL
        ),
        "level_up_color": se.Setting(
            "Level up color",
            "The color to use to highlight the facilities that will level up a ramen expertise.",
            "#FFA30D",
            se.SettingType.COLOR
        ),
    }

class RamenExpertiseRow(hte.Row):
    long_name = "Ramen Expertise"
    short_name = "Expertise"
    description = "[Scenario-specific] Displays the amount of Ramen Expertise gained for each training facility."

    def __init__(self):
        super().__init__()
        self.settings = RamenExpertiseSettings()

    def generate_row_cells(self, game_state, feeling_id: str) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 14:
            return []
        feeling_id_to_name = {
            '1': 'Noodles',
            '2': 'Stock',
            '3': 'Toppings'
        }
        img_name = feeling_id_to_name[feeling_id].lower()
        img_path = util.get_ramen_image_dict()[img_name]
        img = f"<img src=\"{img_path}\" height=\"24\" width=\"24\" style=\"height:24px;width:auto;\" />"


        cells = [hte.Cell(img, title=feeling_id_to_name.get(feeling_id, "Unknown"))]
        for command_key, command_data in game_state.items():
            expertise_gain = next((x['turn'] for x in command_data['feeling_turn_array'] if x['feeling_id'] == int(feeling_id)), 0)
            expertise_left = next((x['remain_turn'] for x in command_data['feeling_turn_info_array'] if x['feeling_id'] == int(feeling_id)), 0)
            is_level_up = expertise_gain >= expertise_left
            if is_level_up and self.settings.highlight_level_up.value:
                cells.append(hte.Cell(f'{expertise_gain if not is_level_up else expertise_left}', bold=is_level_up, color=self.settings.level_up_color.value))
            else:
                cells.append(hte.Cell(f'{expertise_gain if not is_level_up else expertise_left}'))
        return cells

    def to_tr(self, game_state):
        if list(game_state.values())[0]['scenario_id'] != 14:
            return ""
        # Hide if no data (URA) finale
        has_data = True
        for command_key, command_data in game_state.items():
            if not 'feeling_turn_array' in command_data or not 'feeling_turn_info_array' in command_data:
                has_data = False
            elif command_data['feeling_turn_array'] == [] or command_data['feeling_turn_info_array'] == []:
                has_data = False
        if not has_data:
            return ""
        # This actually generates 3 rows, so we need to override the default behavior
        td1 = ''.join(cell.to_td() for cell in self.generate_row_cells(game_state, '1'))
        td2 = ''.join(cell.to_td() for cell in self.generate_row_cells(game_state, '2'))
        td3 = ''.join(cell.to_td() for cell in self.generate_row_cells(game_state, '3'))
        return f'<tr>{td1}</tr><tr>{td2}</tr><tr>{td3}</tr>'

def generate_div(member):
    cell_text = "<div style=\"display: flex; flex-direction: column; align-items: center; justify-content: center;\">"
    chara_id = member['chara_id']
    gain_xp = member['gain_exp']
    chara_img = f"https://gametora.com/images/umamusume/characters/icons/chr_icon_{chara_id}.png"
    gain_img = util.get_dreams_image_dict()[str(gain_xp)]  # TODO use the other PNG if the level is maxed
    cell_text += f"<div style=\"display: flex; flex-direction: column; align-items: center; justify-content: center;\"><img src=\"{chara_img}\" height=\"36\" width=\"36\" style=\"margin-bottom: -2px\" />"
    cell_text += f"""<img src=\"{gain_img}\"height=\"19\" width=\"19\" style=\"position: relative; top: -12px; right: -12px; margin-bottom: -10px\" /></div>"""
    cell_text += "</div>"
    return cell_text


class DreamsPartnersRow(hte.Row):
    long_name = "Beyond Dreams team member Dream Gauge gain"
    short_name = "Dream Gauge"
    description = "[Scenario-specific] Shows the Dream Gauge gain for each team member. Hidden in other scenarios."

    def _generate_cells(self, game_state) -> list[hte.Cell]:
        if list(game_state.values())[0]['scenario_id'] != 13:
            return []

        cells = [hte.Cell(self.short_name, title=self.description)]


        for command_key, command_data in game_state.items():
            cell_text = f"<div style=\"display: flex; align-items: center; justify-content: center; gap: 0.2rem;\">"
            if len(command_data['team_member_info_array']) == 3:
                divs = [generate_div(member) for member in command_data['team_member_info_array']]
                cell_text += "<div>"
                cell_text +=  divs[0]
                cell_text += "<div style=\"display: flex; position: relative; top: -16px; margin-bottom:-16px; z-index:-1;\">" + divs[1] + divs[2] +  "</div>"
                cell_text += "</div>"
            else:
                for member in command_data['team_member_info_array']:
                    cell_text += generate_div(member)

            cell_text += "</div>"
            cells.append(hte.Cell(cell_text))


        return cells

    def to_tr(self, command_info):
        if list(command_info.values())[0]['scenario_id'] != 13:
            return ""

        return super().to_tr(command_info)



class RowTypes(Enum):
    CURRENT_STATS = CurrentStatsRow
    GAINED_STATS = GainedStatsRow
    GAINED_STATS_DISTR = GainedStatsDistributionRow
    GAINED_ENERGY = GainedEnergyRow
    USEFUL_BOND = UsefulBondRow
    TOTAL_BOND = TotalBondRow
    GAINED_SKILLPT = GainedSkillptRow
    FAIL_PERCENTAGE = FailPercentageRow
    LEVEL = LevelRow
    PARTNER_COUNT = PartnerCountRow
    USEFUL_PARTNER_COUNT = UsefulPartnerCountRow
    SKILL_HINT_COUNT = HintCountRow
    RAINBOW_COUNT = RainbowCountRow
    AOHARU_USEFUL_UNITY_PARTNER_COUNT = UsefulUnityTrainingCountRow
    AOHARU_UNITY_PARTNER_COUNT = UnityTrainingCountRow
    AOHARU_UNITY_SCORE = UnityScoreRow
    GL_TOKENS = GrandLiveTokensDistributionRow
    GL_TOKENS_TOTAL = GrandLiveTotalTokensRow
    GM_FRAGMENTS = GrandMastersFragmentsRow
    LARC_STAR_GAUGE_GAIN = LArcStarGaugeGainRow
    LARC_APTITUDE_POINTS = LArcAptitudePointsRow
    UAF_SPORT_POINT_GAIN = UAFSportPointGainRow
    ENERGY_RATIO = EnergyRatio
    GFF_VEGETABLES = GFFVegetablesRow
    GFF_VEGETABLES_DIST = GFFVegetablesDistributionRow
    RMU_RESEARCH = RMUTotalResearchLevelRow
    RMU_RESEARCH_DIST = RMUResearchDistributionRow
    DYI_POINTS_DIST = DYIPointsDistributionRow
    ONSEN_POINTS_DIST = OnsenPointsDistributionRow
    DREAM_PARTNERS = DreamsPartnersRow
    DP_GAIN = DreamPointsRow
    RAMEN_EXPERTISE = RamenExpertiseRow


class DefaultPreset(hte.Preset):
    name = "Default"
    rows = [
        RowTypes.GL_TOKENS,
        RowTypes.GM_FRAGMENTS,
        RowTypes.LARC_APTITUDE_POINTS,
        RowTypes.LARC_STAR_GAUGE_GAIN,
        RowTypes.UAF_SPORT_POINT_GAIN,
        RowTypes.GFF_VEGETABLES,
        RowTypes.RMU_RESEARCH,
        RowTypes.AOHARU_UNITY_SCORE,
        RowTypes.DYI_POINTS_DIST,
        RowTypes.ONSEN_POINTS_DIST,
        RowTypes.DREAM_PARTNERS,
        RowTypes.DP_GAIN,
        RowTypes.RAMEN_EXPERTISE,
        RowTypes.CURRENT_STATS,
        RowTypes.GAINED_STATS,
        RowTypes.USEFUL_BOND,
        RowTypes.GAINED_SKILLPT,
        RowTypes.FAIL_PERCENTAGE,
    ]
