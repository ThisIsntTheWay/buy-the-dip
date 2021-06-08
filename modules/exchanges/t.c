#include <sourcemod>
#include <tf2_stocks>
// ^ tf2_stocks.inc itself includes sdktools.inc and tf2.inc
ConVar c_Jarate;
ConVar c_Milk;
#pragma semicolon 1

#define PLUGIN_VERSION "1.0"

public Plugin myinfo = 
{
	name = "[KTBM]Jarate/Milk Duration",
	author = "kingo",
	description = "Change the duration of jarate/milk via ConVar",
	version = PLUGIN_VERSION,
	url = "kingo.tf"
};

public APLRes AskPluginLoad2(Handle myself, bool late, char[] error, int err_max)
{
	EngineVersion g_engineversion = GetEngineVersion();
	if (g_engineversion != Engine_TF2)
	{
		SetFailState("This plugin was made for use with Team Fortress 2 only.");
	}
} 

public void OnPluginStart()
{
	CreateConVar("sm_jarate_milk_duration_version", PLUGIN_VERSION, "Standard plugin version ConVar. Please don't change me!", FCVAR_REPLICATED|FCVAR_NOTIFY|FCVAR_DONTRECORD);
	c_Jarate = CreateConVar("sm_jarate_duration", "8.0", "Float value in seconds", FCVAR_REPLICATED | FCVAR_NOTIFY | FCVAR_DONTRECORD);
	c_Milk = CreateConVar("sm_milk_duration", "8.0", "Float value in seconds", FCVAR_REPLICATED | FCVAR_NOTIFY | FCVAR_DONTRECORD);
	
	HookUserMessage(GetUserMessageId("PlayerJarated"), event_jarated);
}

public Action:event_jarated(UserMsg:msg_id, Handle:bf, const players[], playersNum, bool:reliable, bool:init)
{
    new client = BfReadByte(bf);
    new victim = BfReadByte(bf);
    new jarType = GetPlayerWeaponSlot(client, TFWeaponSlot_Secondary);
    float jarateTime = GetConVarFloat(c_Jarate);
    float milkTime = GetConVarFloat(c_Milk);
    
    if(IsValidEntity(jarType))
    {
    	char slot1[64];
    	GetEdictClassname(jarType, slot1, sizeof(slot1));
    	if(strcmp(slot1, "tf_weapon_jar", false) == 0)
    	{
			// print to console HERE

    		TF2_RemoveCondition(victim, TFCond_Jarated);
    		TF2_AddCondition(victim, TFCond_Jarated, jarateTime);
    	}
    	else if(strcmp(slot1, "tf_weapon_jar_milk", false) == 0)
    	{
			// print to console HERE
			
    		TF2_RemoveCondition(victim, TFCond_Milked);
    		TF2_AddCondition(victim, TFCond_Milked, milkTime);
    	}
    }
/*   
    if(TF2_IsPlayerInCondition(victim, TFCond_Jarated) && TF2_IsPlayerInCondition(victim, TFCond_Milked))
    {
    	TF2_RemoveCondition(victim, TFCond_Jarated);
    	TF2_RemoveCondition(victim, TFCond_Milked);
    	TF2_Addcondition(victim, TFCond_Jarated, jarateTime);
    	TF2_AddCondition(victim, TFCond_Milked, milkTime);
    }
    else if (TF2_IsPlayerInCondition(victim, TFCond_Jarated))
    {
    	TF2_RemoveCondition(victim, TFCond_Jarated);
    	TF2_Addcondition(victim, TFCond_Jarated, jarateTime);
    }
    else if (TF2_IsPlayerInCondition(victim, TFCond_Milked))
    {
    	TF2_RemoveCondition(victim, TFCond_Milked);
    	TF2_Addcondition(victim, TFCond_Milked, milkTime);
    }

    return Plugin_Continue; */
}