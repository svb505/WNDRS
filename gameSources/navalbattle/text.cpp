#include <windows.h>
#include <GL/gl.h>
#include <iostream>

GLuint fontBase;

void InitFont() {
    HDC hdc = wglGetCurrentDC();
    if (!hdc) std::cout << "HDC is NULL\n";
    HFONT font = CreateFontA(
        -16, 0, 0, 0,
        FW_NORMAL,
        FALSE, FALSE, FALSE,
        ANSI_CHARSET,
        OUT_TT_PRECIS,
        CLIP_DEFAULT_PRECIS,
        ANTIALIASED_QUALITY,
        FF_DONTCARE | DEFAULT_PITCH,
        "Arial"
    );

    SelectObject(hdc, font);

    fontBase = glGenLists(256);
    wglUseFontBitmaps(hdc, 0, 255, fontBase);
}
void drawText(float x, float y, const std::string& text) {
    glRasterPos2f(x, y);

    glPushAttrib(GL_LIST_BIT);
    glListBase(fontBase);

    glCallLists(text.size(), GL_UNSIGNED_BYTE, text.c_str());

    glPopAttrib();
}