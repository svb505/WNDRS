#pragma once
#include "svbmath.h"
#include <vector>
#include "model.h"
#include "camera.h"
#include <map>
#include <memory>

enum class DecType {
	BUILD1,
	BUILD2,
	TREE,
	LAMP,
	STREET
};

struct DecorationInstance{
	DecType type;
	svbmath::Vec3 position;
	float rotationY;
};

extern std::map<DecType, float> scales;

class Decorations {
private:
	int buildsCount = 4;
	int treesCount = 4;
	int lampsCount = 5;
	float buildXStep = 25.0f;

	std::vector<svbmath::Vec3> allPositions;
	
	svbmath::Vec3 buildBasePos = {0.0f,0.0f,0.0f};
	std::vector<DecorationInstance> decorations;

	std::map<DecType, std::unique_ptr<OBJModel>> models;
public:
	void addDecoration(DecType type,svbmath::Vec3 pos,float rotationY);
	void addBuildings();
	void addEndBuildings();
	void addTrees();
	void addLamps();
	Bounds getWorldBounds(const OBJModel& model, const DecorationInstance& decoration);
	void initDecoration(const std::string& modelPath, DecType decType,const std::string& texturePath);
	void initPositions();
	void drawAllDecorations(DecType decType);
	bool checkCollision(Camera& cam, DecType decType);
};