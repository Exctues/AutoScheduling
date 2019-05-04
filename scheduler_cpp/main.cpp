//
// Created by Vyacheslav on 01.05.2019.
//

#include "Algorithm/Configuration.h"
#include "Algorithm/Room.h"
#include "Algorithm/Schedule.h"
#include <nlohmann/json.hpp>
#include <iostream>

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Forgot to specify path to the configuration file\n";
        return 1;
    }

    string path_string = argv[1];
    char* path = (char*) path_string.c_str();
    Configuration::GetInstance().ParseFile( path );

    Algorithm::GetInstance().Start();

    Schedule* best = Algorithm::GetInstance().GetBestChromosome();
    nlohmann::json output;
    for (auto lesson : best->GetClasses()) {
        auto groups = lesson.first->GetGroups();
        for (auto group : groups) {
            nlohmann::json lesson_json;
            lesson_json["Course_name"] = lesson.first->GetCourse().GetName();
            if (lesson.first->IsLabRequired()) {
                lesson_json["Lesson_type"] = "Lab";
            } else if (lesson.first->IsTutorial()) {
                lesson_json["Lesson_type"] = "Tutorial";
            } else {
                lesson_json["Lesson_type"] = "Lecture";
            }
            lesson_json["Faculty"] = lesson.first->GetProfessor().GetName();
            lesson_json["Group"] = group->GetName();
            int pos = lesson.second;

            int rooms_number = Configuration::GetInstance().GetNumberOfRooms();
            int day_id = pos / rooms_number / DAY_HOURS;
            pos -= day_id * rooms_number * DAY_HOURS;
            int room_id = pos / DAY_HOURS;
            int time_id = pos - room_id * DAY_HOURS;
            string day = Configuration::GetInstance().GetDayById(day_id);
            string time = Configuration::GetInstance().GetTimeById(time_id);
            string room = Configuration::GetInstance().GetRoomById(room_id)->GetName();
            lesson_json["Day"] = day;
            lesson_json["Time"] = time;
            lesson_json["Auditorium"] = room;
            output.push_back(lesson_json);
        }
    }

    std::cout << output;
    return 0;
}