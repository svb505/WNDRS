#include "days.h"
#include "variables.h"

int day = 0;
int heure = 0;
float seconds = 0;

void countDays(float dt) {
	seconds += (dt * 2);

	if (seconds >= 60.0f) {
		heure++;
		seconds = 0.0f;
	}
	if (heure > 23) {
		day++;
		heure = 0;
		sallesForDay = 0;
	}
}