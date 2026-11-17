#include <vector>
#include <random>
#include "svbRandom.h"

float returnRandomNum(float min, float max) {
    std::random_device rd;
    static std::mt19937 gen(rd());

    std::uniform_real_distribution<float> randomN(min, max);

    return randomN(gen);

}
