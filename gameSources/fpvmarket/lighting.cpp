#include <windows.h>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include "lighting.h"

LightingSettings indoorLight = {
	{ 0.80f, 0.80f, 0.80f, 1.0f },
	{ 0.80f, 0.80f, 0.80f, 1.0f },
	{ 1.0f, 1.0f, 1.0f, 1.0f }
};

LightingSettings outdoorDayLight = {
	{ 0.35f, 0.40f, 0.50f, 1.0f },
	{ 1.00f, 0.95f, 0.85f, 1.0f },
	{ 0.80f, 0.80f, 0.80f, 1.0f }
};

LightingSettings outdoorNightLight = {
	{ 0.15f, 0.15f, 0.15f, 1.0f },
	{ 0.15f, 0.15f, 0.15f, 1.0f },
	{ 1.0f, 1.0f, 1.0f, 1.0f }
};

void initLighting() {
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glEnable(GL_COLOR_MATERIAL);

	GLfloat lightPos[] = { 0.0f, 2.0f,-10.0f, 1.0f }; //x,y,z,type 
	GLfloat lightAmbient[] = { 0.8f, 0.8f,0.8f,
		1.0f };//Background color r,g,b,a 
	GLfloat lightDiffuse[] = { 0.8f, 0.8f, 0.8f,
		1.0f };//Diffuse light r,g,b,a 
	GLfloat lightSpec[] = { 1.0f, 1.0f, 1.0f, 1.0f };//Specular reflection r,g,b,a

	glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
	glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpec);
	glEnable(GL_DEPTH_TEST);
}

void setLighting(const LightingSettings& light){
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);

	glLightfv(GL_LIGHT0, GL_AMBIENT, light.ambient);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light.diffuse);
	glLightfv(GL_LIGHT0, GL_SPECULAR, light.specular);
}
