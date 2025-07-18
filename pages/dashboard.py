from nicegui import ui, app

from utils.tree import build_tree, get_mapping_and_grouping_list

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def dashboard():
    right_drawer: ui.right_drawer = app.storage.client["right_drawer"]
    right_drawer_rendered_by = app.storage.client["right_drawer_rendered_by"]
    brokers_df = app.storage.client["brokers_df"]
    accounts_df = app.storage.client["accounts_df"]

    tree_enum_mapping, grouping_list = get_mapping_and_grouping_list(brokers_df)

    # with ui.row().classes("mb-5"):
    #     with ui.card().classes("h-32 w-64"):
    #         ui.label("Metric 1")
    #     with ui.card().classes("h-32 w-64"):
    #         ui.label("Metric 1")
    #
    # ui.separator().classes("mb-5")

    with ui.row().classes("w-full justify-between mb-4"):
        with ui.dropdown_button("Select Accounts(s)", icon="business_center"):
            with ui.column().classes("w-full p-4"):
                grouping_select = ui.select(grouping_list, multiple=True, label="Grouping", with_input=True, clearable=True, value=grouping_list[0]).props("outlined use-chips").classes("w-full")
                with grouping_select.add_slot("prepend"):
                    ui.icon("account_tree")
                with ui.row().classes("w-full justify-between items-center"):
                    ui.label("Select Account(s)")
                    with ui.button_group().props("flat").classes("bg-grey-2 text-grey-14"):
                        tree_select_all_btn = ui.button(icon="select_all", color="text-grey-14").props("flat dense")
                        tree_deselect_all_btn = ui.button(icon="deselect", color="text-grey-14").props("flat dense")
                        tree_expand_btn = ui.button(icon="add", color="text-grey-14").props("flat dense")
                        tree_collapse_btn = ui.button(icon="remove", color="text-grey-14").props("flat dense")

                account_tree = (
                    ui.tree(
                        build_tree(accounts_df, grouping_list[:1], enum_mapping=tree_enum_mapping, ungroup_keys=grouping_list[1:]),
                        label_key="label",
                        tick_strategy="leaf",
                    )
                    .classes("w-full")
                    .expand()
                )

                def on_grouping_change(e):
                    grouping_keys = e.value
                    ungrouped_keys = list(set(grouping_list) - set(grouping_keys))
                    account_tree._props["nodes"] = build_tree(accounts_df, grouping_keys, enum_mapping=tree_enum_mapping, ungroup_keys=ungrouped_keys)
                    account_tree.update()
                    account_tree.expand()

                grouping_select.on_value_change(on_grouping_change)
                tree_expand_btn.on_click(account_tree.expand)
                tree_collapse_btn.on_click(account_tree.collapse)
                tree_select_all_btn.on_click(account_tree.tick)
                tree_deselect_all_btn.on_click(account_tree.untick)

        ui.toggle(["Value", "Percent"])

    with ui.row().classes("mb-2"):
        with ui.grid(columns=7, rows=1).classes("mr-5"):
            for weekday in WEEKDAYS:
                ui.label(weekday).classes("text-md w-32 pl-2")
        ui.label("Week").classes("text-md w-32 pl-2")
    with ui.row().classes("w-full"):
        with ui.grid(columns=7, rows=6).classes("mr-5"):
            for i in range(1, 36):
                with ui.card().classes("h-32 w-32"):
                    ui.label(f"Day {i}")
        with ui.grid(columns=1, rows=6):
            for i in range(1, 6):
                with ui.card().classes("h-32 w-32"):
                    ui.label(f"Week {i}")

    if right_drawer and right_drawer_rendered_by != "dashboard":
        right_drawer.clear()
        app.storage.client["right_drawer_rendered_by"] = "dashboard"
        with right_drawer:
            ui.label("Right Drawer for Dashboard").classes("text-lg")
            ui.button("Close", on_click=lambda: right_drawer.toggle())
