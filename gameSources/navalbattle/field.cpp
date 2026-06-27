#include <map>
#include <string>
#include "field.h"
#include <format>
#include <GLFW/glfw3.h>
#include "text.h"

const std::map<std::string, Cellule>& Field::getField(const FieldType& type) const{
	return (type == FieldType::Enemy) ? fieldEnemy : fieldPlayer;
}

std::map<std::string, Cellule>& Field::getField(const FieldType& type){
	return (type == FieldType::Enemy) ? fieldEnemy : fieldPlayer;
}
void Field::setupField() {
	for (int x = 0; x < 9; x++) {
		for (int y = 0; y < 10; y++) {
			std::string name = std::format("{}{}",letters[x],numbers[y]);

			fieldPlayer[name] = { false,false };
			fieldEnemy[name] = { false,false };
		}
	}
}
CellPos Field::getPlayerCellPos(const std::string& name,const FieldType& type){
	float minX; 

	if (type == FieldType::Player) minX = -900.0f;
	else minX = 1000.0f;  

	int col = name[0] - 'A';
	col = 8 - col;

	int row = std::stoi(name.substr(1)) - 1;
	

	if (type == FieldType::Player) return { minX + col * 100.0f + 50.0f, 500.0f - (row + 1) * 100.0f + 50.0f };
	else return { minX - col * 100.0f - 50.0f, 500.0f - row * 100.0f - 50.0f };

}
void Field::draw() {
	glColor3f(1.0f,1.0f,1.0f);
	glLineWidth(2.0f);


	glBegin(GL_LINES);

	for (int i = 0; i < 10; i++) {
		glVertex2f(-900.0f, -500.0f + 100 * i);
		glVertex2f(0.0f, -500.0f + 100 * i);

		glVertex2f(-900.0f + 100 * i, -500.0f);
		glVertex2f(-900.0f + 100 * i, 500.0f);	
	}

	for (int i = 0; i < 10; i++) {
		glVertex2f(100.0f, 500.0f - 100 * i);
		glVertex2f(1000.0f, 500.0f - 100 * i);

		glVertex2f(1000.0f - 100 * i, -500.0f);
		glVertex2f(1000.0f - 100 * i, 500.0f);
	}


	glVertex2f(-900.0f, 500.0f);
	glVertex2f(0.0f, 500.0f);

	glVertex2f(100.0f, -500.0f);
	glVertex2f(1000.0f, -500.0f);

	glEnd();

	for (int i = 0; i < 10; i++) {
		drawText(-940.0f, 420.0f - 100 * i,std::to_string(i + 1));
		drawText(-850.0f + 100 * i, 520.0f, letters[i]);

		drawText(60.0f, 420.0f - 100 * i, std::to_string(i + 1));
		drawText(150.0f + 100 * i, 520.0f, letters[i]);
	}

	/*CellPos p = getPlayerCellPos("C4", FieldType::Enemy);

	glColor3f(1.0f, 0.0f, 0.0f);
	glPointSize(15.0f);
	glBegin(GL_POINTS);

	glVertex2f(p.x, p.y);

	glEnd();*/
}