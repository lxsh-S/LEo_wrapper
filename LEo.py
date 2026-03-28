from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.theme import Theme
from textual.widgets import Header, Footer, Input, Markdown
from base import chat, history
import asyncio

TOKYO_NIGHT = Theme(
    name="tokyo-night",
    primary="#7aa2f7",
    secondary="#bb9af7",
    accent="#ff9e64",
    background="#16161e",
    surface="#1a1b2e",
    panel="#1f2335",
    foreground="#c0caf5",
    success="#9ece6a",
    warning="#e0af68",
    error="#f7768e",
    dark=True,
)


class LEo(App):
    CSS_PATH = "config.css"

    

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, icon="🦁")
        with VerticalScroll(id="chat-view"):
            pass
        yield Input(placeholder="Whisper to LEo...", type="text", id="usr_input")
        yield Footer()

    @on(Input.Submitted)
    async def accept_usr_input(self):
        input = self.query_one(Input)
        usr_msg = input.value
        if not usr_msg.strip():
            return

        chat_view = self.query_one("#chat-view", VerticalScroll)

        user_md = Markdown(f"**you:** {usr_msg}")
        user_md.add_class("user-msg")
        await chat_view.mount(user_md)

        ai_md = Markdown(f"**LEo:** ")
        ai_md.add_class("leo-response")
        await chat_view.mount(ai_md)

        input.clear()
        input.focus()

        # stream chunks into the markdown widget
        stream = chat(usr_msg)
        reply = ""
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            reply += token
            await ai_md.update(f"**LEo:** {reply}")
            chat_view.scroll_end(animate=False)
            await asyncio.sleep(0)

        history.append({"role": "assistant", "content": reply})

    def on_mount(self) -> None:
        self.register_theme(TOKYO_NIGHT)
        self.theme = "tokyo-night"
        self.title = "LEo"
        self.sub_title = "v0.0.2"
        self.query_one(Input).focus()

