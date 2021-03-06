/*************** SDCC fucntion address ***************/
#define SDCCMAP_cg_simpleProfileChangeCB                   0x8800
#define SDCCMAP_cg_accelEnablerChangeCB                    0x8832
#define SDCCMAP_cg_battProfileChangeCB                     0x888e
#define SDCCMAP_cg_EVT_1_CB                                0x888f
#define SDCCMAP_cg_EVT_2_CB                                0x88b3
#define SDCCMAP_cg_EVT_3_CB                                0x88b4
#define SDCCMAP_cg_EVT_4_CB                                0x88b5
#define SDCCMAP_cg_timeserviceChangeCB                     0x88b6
#define SDCCMAP_rtcInit                                    0x8a26
#define SDCCMAP_rtcSetTime                                 0x8a2a
#define SDCCMAP_rtcGetTime                                 0x8a46
#define SDCCMAP_rtcSetDate                                 0x8a85
#define SDCCMAP_rtcGetDate                                 0x8aa5
#define SDCCMAP_rtcGetAlarm                                0x8ae9
#define SDCCMAP_rtcSetAlarm                                0x8b2d
#define SDCCMAP_Accel_AddService                           0x8b6d
#define SDCCMAP_Accel_RegisterAppCBs                       0x8b7a
#define SDCCMAP_Accel_SetParameter                         0x8b84
#define SDCCMAP_Accel_GetParameter                         0x8ba4
#define SDCCMAP_osalTimerInit                              0x8bc2
#define SDCCMAP_osal_start_timerEx                         0x8bc6
#define SDCCMAP_osal_start_reload_timer                    0x8c0c
#define SDCCMAP_osal_stop_timerEx                          0x8c52
#define SDCCMAP_osal_get_timeoutEx                         0x8c70
#define SDCCMAP_osal_timer_ISR                             0x8c93
#define SDCCMAP_osal_adjust_timers                         0x8c94
#define SDCCMAP_osalTimerUpdate                            0x8c95
#define SDCCMAP_osal_timer_num_active                      0x8ca0
#define SDCCMAP_osal_sleep_timers                          0x8ca1
#define SDCCMAP_osal_unsleep_timers                        0x8ca2
#define SDCCMAP_osal_GetSystemClock                        0x8ca3
#define SDCCMAP_osal_next_timeout                          0x8cae
#define SDCCMAP_accInit                                    0x8caf
#define SDCCMAP_accWriteReg                                0x8cb3
#define SDCCMAP_accReadReg                                 0x8cc7
#define SDCCMAP_accReadMultiReg                            0x8ce3
#define SDCCMAP_accReadAcc                                 0x8ceb
#define SDCCMAP_accReadAllAcc                              0x8d2a
#define SDCCMAP_accSetFreeFallEvent                        0x8d2b
#define SDCCMAP_timeservice_AddService                     0x8d2f
#define SDCCMAP_timeservice_RegisterAppCBs                 0x8d3c
#define SDCCMAP_timeservice_SetParameter                   0x8d46
#define SDCCMAP_timeservice_GetParameter                   0x8d66
#define SDCCMAP_SimpleProfile_AddService                   0x8d84
#define SDCCMAP_SimpleProfile_RegisterAppCBs               0x8d91
#define SDCCMAP_SimpleProfile_SetParameter                 0x8d9b
#define SDCCMAP_SimpleProfile_GetParameter                 0x8dbb
