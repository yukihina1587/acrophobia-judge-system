cmake_minimum_required(VERSION 3.14)
project(MindWaveMobile2)

set(CMAKE_CXX_STANDARD 14)

include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Release")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/libs")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/libs/win32")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/libs/x64")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/win32/thinkgear_testapp/Debug")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/win32/thinkgear_testapp/thinkgear_testapp")
include_directories("Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/x64/thinkgear_testapp/thinkgear_testapp")

add_executable(MindWaveMobile2
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Release/Algo SDK Sample.pch"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Algo SDK Sample.cpp"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Algo SDK Sample.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Get-EEG-C++.cpp"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/Resource.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/stdafx.cpp"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/stdafx.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/targetver.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Algo SDK Sample/Algo SDK Sample/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include/NSK_Algo.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include/NSK_Algo_Defines.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include/NSK_Algo_Helper.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include/NSK_Algo_ReturnCodes.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/EEG_Algo_SDK_Windows/Include/Platform_defines.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/libs/win32/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/libs/x64/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/win32/thinkgear_testapp/Debug/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/win32/thinkgear_testapp/thinkgear_testapp/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/win32/thinkgear_testapp/thinkgear_testapp/thinkgear_testapp.c"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/x64/thinkgear_testapp/thinkgear_testapp/thinkgear.h"
        "Windows-Developer-Tools-3.2/Windows Developer Tools 3.2/Stream SDK for PC/Sample Project/x64/thinkgear_testapp/thinkgear_testapp/thinkgear_testapp.c")
