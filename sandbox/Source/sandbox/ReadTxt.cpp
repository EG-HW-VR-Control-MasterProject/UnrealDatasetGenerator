// Fill out your copyright notice in the Description page of Project Settings.


#include "ReadTxt.h"

// Fill out your copyright notice in the Description page of Project Settings.
#include <Runtime/Core/Public/Misc/Paths.h>
#include <Runtime/Core/Public/HAL/PlatformFilemanager.h>

FString UReadTxt::LoadFileToString(FString Filename)
{
	FString directory = FPaths::GameDevelopersDir();
	FString Result;


	IPlatformFile& file = FPlatformFileManager::Get().GetPlatformFile();

	if (file.CreateDirectory(*directory))
	{
		FString myFile = directory + "/" + Filename;
		FFileHelper::LoadFileToString(Result, *myFile);


	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("NOT Works"));
	}

	return Result;
}

