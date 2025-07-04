from nicegui import ui, app


def accounts():
    right_drawer: ui.right_drawer = app.storage.client["right_drawer"]
    right_drawer_rendered_by = app.storage.client["right_drawer_rendered_by"]
    state = {"width": 300, "text": "My Val Test"}

    def on_width_change(value):
        state["width"] = value
        right_drawer.props(f"width={state['width']}")

    with ui.column().classes("w-full h-full text-lg"):
        ui.markdown("## 💼 Accounts")
        ui.label("Manage your trading accounts")
        ui.space()

        with ui.row().classes("w-full"):
            ui.button("Add Account", on_click=lambda: ui.notify("Add Account clicked"))
            ui.button("Archive Account", on_click=lambda: ui.notify("Archive Account clicked")).props("disabled")
            ui.button("Edit Account", on_click=lambda: ui.notify("Edit Account clicked")).props("disabled")
        ui.space()

        ui.button("Toggle Right Drawer", on_click=lambda: right_drawer.clear()).classes("mt-4")
        ui.space()

        def raise_exception():
            raise Exception("This is an exception")

        ui.label().classes("text-center").bind_text_from(state, "text", backward=lambda x: f"Current Text: {x}").classes("m-2")
        ui.button("Raise Exception", on_click=raise_exception).classes("mt-4")

        if right_drawer and right_drawer_rendered_by != "accounts":
            app.storage.client["right_drawer_rendered_by"] = "accounts"
            right_drawer.clear()
            with right_drawer:
                ui.label("Right Drawer for Accounts").classes("text-lg")
                ui.button("Close", on_click=lambda: right_drawer.toggle())
                ui.slider(min=300, max=800, value=state["width"], step=10, on_change=lambda e: on_width_change(e.value)).classes("m-2").props("color=primary").bind_value(state, "width")
                ui.input(
                    label="Right Drawer Account Text",
                    value="",
                ).classes("m-2").props(
                    "color=primary"
                ).bind_value(state, "text")
                ui.label().bind_text_from(state, "text", backward=lambda x: f"Current Text: {x}").classes("m-2")
