#include <iostream>

#include <sndfile.h>


#include "noise_gate/noise_gate.hpp"

int main(int argc, char* argv[]) {
    if (argc == 1) {
        std::cout << craft_greeting("C++20") << std::endl;
        return 0;
    }

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <path_to_audio_file>" << std::endl;
        return 1;
    }

    const auto* file_path = argv[1];

    SF_INFO fileInfo;
    auto* audioFile = sf_open(file_path, SFM_READ, &fileInfo);

    if (!audioFile) {
        std::cerr << "Error: Could not open file: " << file_path << std::endl;
        std::cerr << "libsndfile error: " << sf_strerror(nullptr) << std::endl;
        return 1;
    }

    std::cout << "Successfully opened audio file: " << file_path << std::endl;
    std::cout << "------------------------------------" << std::endl;
    std::cout << "  Sample Rate: " << fileInfo.samplerate << " Hz" << std::endl;
    std::cout << "  Channels:    " << fileInfo.channels << std::endl;
    std::cout << "  Frames:      " << fileInfo.frames << " (total samples per channel)" << std::endl;
    std::cout << "  Format Code: 0x" << std::hex << fileInfo.format << std::dec << std::endl;
    std::cout << "------------------------------------" << std::endl;

    sf_close(audioFile);

    return 0;
}
