import keyboard

from epta.tools.hookers.keyboard_hookers import KeyboardHooker


class KeyboardAppController(KeyboardHooker):
    def __init__(self, config: 'Config', app_states: dict, name: str = 'kbd_app_controller', **kwargs):
        super(KeyboardAppController, self).__init__(config=config, name=name, **kwargs)

        # working_state:
        # 0 - off, 1 - on

        # render_state:
        # 0 - nothing, 1 - head, 2 - 1 + skeleton, 3 - 2 + bbox

        # active_state:
        # 0 - aim off, 1 - aim on

        # exit:
        # 1 - app off, 0 - app on
        self.app_states = app_states

        self._add_hotkeys()

    def set_state(self, state_name: str, **kwargs):
        state = self.app_states.get(state_name, 0)
        if state_name == 'working_state':
            state = (state + 1) % 2
        elif state_name == 'render_state':
            state = (state + 1) % 4
        elif state_name == 'active_state':
            state = (state + 1) % 2
        elif state_name == 'exit':
            state = 1
        self.app_states[state_name] = state
        print(f'{state_name} state is set to', state)

    def _add_hotkeys(self):
        keyboard.add_hotkey(self.config.settings.working_state_key, self.set_state, args=('working_state',))
        keyboard.add_hotkey(self.config.settings.render_state_key, self.set_state, args=('render_state',))
        keyboard.add_hotkey(self.config.settings.active_state_key, self.set_state, args=('active_state',))
        keyboard.add_hotkey(self.config.settings.exit_state_key, self.set_state, args=('exit',))
