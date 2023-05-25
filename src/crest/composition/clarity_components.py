# pylint: disable=too-many-lines
"""
Module containing the definition of all Clarity components and the list of
disallowed composition of Clarity components.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT
import dataclasses
import enum
from typing import Tuple


@dataclasses.dataclass(frozen=True)
class Component:
    """
    A Clarity component, defined by an arbitrary name and a tuple of CSS
    selectors by which it can be identified.
    """

    name: str
    css_selectors: Tuple[str, ...]


class Components(enum.Enum):
    """
    Enum of all Clarity components supported.
    """
    ACCORDION = Component("accordion", ("clr-accordion",))
    ALERT = Component("alert", ("cds-alert", "clr-alert", "div.alert"))
    BADGE = Component("badge", ("cds-badge", "clr-badge", "span.badge"))
    BUTTON = Component("button", ("cds-button", "clr-button", "button.btn"))
    BUTTON_GROUP = Component("button group", ("div.btn-group",))
    CARD = Component("card", ("a.card", "div.card"))
    CHECKBOX = Component(
        "checkbox",
        (
            "cds-checkbox",
            "clr-checkbox",
            "clr-checkbox-wrapper > input",
            "div.clr-checkbox-wrapper > input",
            "input.clr-checkbox",
        ),
    )
    COMBO_BOX = Component("combo box", ("clr-combobox",))
    DATALIST = Component("datalist", ("cds-datalist", "clr-datalist-container"))
    DATE_PICKER = Component("date picker", ("clr-date-container",))
    DROPDOWN = Component("dropdown", ("clr-dropdown", "div.dropdown"))
    FORM_GROUP = Component("form", ("cds-form-group",))
    HEADER = Component("header", ("header",))
    ICON_BUTTON = Component("icon-button", ("button.btn-icon", "cds-icon-button"))
    INLINE_BUTTON = Component("inline-button", ("cds-inline-button",))
    INPUT = Component(
        "input",
        (
            "cds-input",
            "clr-input-container > input",
            "div.clr-input-wrapper > input",
            "input.clr-input",
            "input[clrInput]",
        ),
    )
    LABEL = Component("label", ("span.label", "a.label"))
    LIST = Component(
        "list",
        (
            "ol.list",
            "ol.list-unstyled",
            "ol[cds-list]",
            "ul.list",
            "ul.list-unstyled",
            "ul[csd-list]",
        ),
    )
    MODAL = Component("modal", ("cds-modal", "clr-modal", "div.modal"))
    PASSWORD = Component(
        "password",
        (
            "cds-password",
            "clr-password-container > input",
            "input[clrPassword]",
            'input[type="password"].clr-input',
        ),
    )
    PROGRESS_BAR = Component(
        "progress bar",
        ("clr-progress-bar", "div.progress > progress", "div.progress-static"),
    )
    RADIO = Component(
        "radio button",
        (
            "cds-radio",
            'clr-radio-wrapper > input[type="radio"]',
            "input.clr-radio",
            "input[clrRadio]",
        ),
    )
    RANGE = Component(
        "range input",
        ("cds-range", "input[clrRange]", 'clr-range-container > input[type="range"]'),
    )
    SELECT = Component(
        "select",
        (
            "cds-select",
            "clr-select-container > select",
            "select.clr-select",
            "select[clrSelect]",
        ),
    )
    SIGNPOST = Component("signpost", ("clr-signpost",))
    SPINNER = Component("spinner", ("span.spinner", "clr-spinner"))
    STACK_VIEW = Component("stack view", ("div.stack-view", "clr-stack-view"))
    STEPPER = Component("stepper", ("form[clrStepper]",))
    TAB = Component("tab", ("clr-tab", 'section[role="tabpanel"]'))
    TABLE = Component("table", ("table.table",))
    TEXTAREA = Component(
        "textarea",
        (
            "cds-textarea",
            "clr-textarea-container > textarea",
            "textarea.clr-textarea",
            "textarea[clrTextarea]",
        ),
    )
    TIMELINE = Component("timeline", ("ul.clr-timeline",))
    TOGGLE = Component(
        "toggle switch",
        (
            "cds-toggle",
            'clr-toggle-wrapper > input[type="checkbox"]',
            "input.clr-toggle",
            "input[clrToggle]",
        ),
    )
    TOOLTIP = Component("tooltip", ("a.tooltip", "clr-tooltip"))
    TREE_VIEW = Component("tree view", ("clr-tree",))
    VERTICAL_NAV = Component("vertical nav", ("clr-vertical-nav",))
