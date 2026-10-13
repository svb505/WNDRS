#pragma once
#include <AL/al.h>
#include <AL/alc.h>
#include <sndfile.h>
#include <iostream>
#include <vector>
#include "map"
#include "svbmath.h"

struct SourceConfig {
    std::string name;
    float gain;
    bool looping = false;

    float refDist = -1.0f;
    float maxDist = -1.0f;
    float rolloff = -1.0f;
};

class Sound {
public:
    bool stepsPlayed = false;

    ALCdevice* audioDevice = nullptr;
    ALCcontext* audioContext = nullptr;

    std::map<std::string, ALuint> buffers = {
        {"City", 0},
        {"Steps", 0}
    };
    std::map<std::string, ALuint> sources = {
        {"City", 0},
        {"Steps", 0}
    };

    void setSourcePosition(ALuint source, svbmath::Vec3 posit) {
        ALfloat pos[] = { posit.x, posit.y, posit.z };
        ALfloat vel[] = { 0.0f, 0.0f, 0.0f };

        alSourcefv(source, AL_POSITION, pos);
        alSourcefv(source, AL_VELOCITY, vel);
    }
    void setListener(svbmath::Vec3 pos, svbmath::Vec3 forwardVector) {
        ALfloat position[] = { pos.x, pos.y, pos.z };
        ALfloat vel[] = { 0.0f, 0.0f, 0.0f };

        ALfloat ori[] = {
            forwardVector.x, forwardVector.y, forwardVector.z,
            0.0f, 1.0f, 0.0f
        };

        alListenerfv(AL_POSITION, position);
        alListenerfv(AL_VELOCITY, vel);
        alListenerfv(AL_ORIENTATION, ori);
    }
    ALuint LoadWav(const char* filename) {
        SF_INFO info{};
        SNDFILE* file = sf_open(filename, SFM_READ, &info);
        if (!file) {
            std::cerr << "Failed to load sound: " << filename << "\n";
            return 0;
        }

        std::vector<short> samples(info.frames * info.channels);
        sf_readf_short(file, samples.data(), info.frames);
        sf_close(file);

        ALuint buffer;
        alGenBuffers(1, &buffer);

        ALenum format =
            (info.channels == 1) ? AL_FORMAT_MONO16 : AL_FORMAT_STEREO16;

        alBufferData(
            buffer,
            format,
            samples.data(),
            (ALsizei)(samples.size() * sizeof(short)),
            info.samplerate
        );

        return buffer;
    }
    void playSound(ALuint source, svbmath::Vec3 posit) {
        setSourcePosition(source, posit);

        alSourceStop(source);

        alSourcePlay(source);
    }
    void setupBuffers() {
        audioDevice = alcOpenDevice(nullptr);
        audioContext = alcCreateContext(audioDevice, nullptr);
        alcMakeContextCurrent(audioContext);

        buffers["City"] = LoadWav("res/sound/city.wav");
        buffers["Steps"] = LoadWav("res/sound/steps.wav");
    }
    void createSources() {
        alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED);

        std::vector<SourceConfig> configs = {
            {"City", 0.5f, true, 4.0f, 80.0f, 2.0f},
            {"Steps", 1.0f, false, 15.0f, 600.0f, 0.6f},
        };

        for (const auto& cfg : configs) {
            alGenSources(1, &sources[cfg.name]);

            alSourcei(sources[cfg.name], AL_BUFFER, buffers[cfg.name]);
            alSourcef(sources[cfg.name], AL_GAIN, cfg.gain);

            if (cfg.looping)
                alSourcei(sources[cfg.name], AL_LOOPING, AL_TRUE);

            if (cfg.refDist > 0.0f)
                alSourcef(sources[cfg.name], AL_REFERENCE_DISTANCE, cfg.refDist);

            if (cfg.maxDist > 0.0f)
                alSourcef(sources[cfg.name], AL_MAX_DISTANCE, cfg.maxDist);

            if (cfg.rolloff > 0.0f)
                alSourcef(sources[cfg.name], AL_ROLLOFF_FACTOR, cfg.rolloff);
        }

        alSourcePlay(sources["City"]);
    }
};

