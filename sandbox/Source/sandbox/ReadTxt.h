// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include <Runtime\Core\Public\Misc\FileHelper.h>
#include "ReadTxt.generated.h"

/**
 * 
 */
UCLASS()
class SANDBOX_API UReadTxt : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()


		UFUNCTION(BlueprintCallable, Category = "File I/O")
		static FString LoadFileToString(FString Filename);

	
};




