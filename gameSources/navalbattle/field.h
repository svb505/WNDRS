#pragma once
#include <map>
#include <string>
#include "vec2.h"

enum class FieldType {
	Player,
	Enemy
};
struct CellPos {
	float x; float y;
};
struct Cellule {
	bool placedShip = false;
	bool hit = false;
};

class Field {
private:
	std::string letters[10] = { "A","B","C","D","E","F","G","H","I"};
	int numbers[10] = { 1,2,3,4,5,6,7,8,9,10 };

	std::map<std::string, Cellule> fieldPlayer;
	std::map<std::string, Cellule> fieldEnemy;
public:
	CellPos getPlayerCellPos(const std::string& name,const FieldType& type);
	const std::map<std::string, Cellule>& getField(const FieldType& type) const;
	std::map<std::string, Cellule>& getField(const FieldType& type);

	void setupField();
	void draw();
};
