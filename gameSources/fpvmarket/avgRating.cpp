#include "avgRating.h"
#include "variables.h"

float averageRating() {
	if (ratings.empty()) return 0.0f;

	float sum = 0.0f;
	for (float r : ratings) sum += r;

	return std::clamp(sum / static_cast<float>(ratings.size()), 0.0f, 5.0f);
}