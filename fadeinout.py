def fade_in(window, alpha=0.0):
    if alpha < 1.0:
        alpha += 0.05
        window.attributes("-alpha", alpha)
        window.after(30, fade_in, window, alpha)
    else:
        window.attributes("-alpha", 1.0)
def fade_out(window, alpha=1.0):
    if alpha > 0:
        alpha -= 0.05
        window.attributes("-alpha", alpha)
        window.after(30, fade_out, window, alpha)
    else:
        window.destroy()