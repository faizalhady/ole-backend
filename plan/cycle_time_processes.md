# Cycle Time — Process & Alias Catalog

> Auto-generated from `data/mart/cycle_time/raw.parquet`.
> Use this to define the **standard process flow** per (customer × line).
> Same `process` code can map to different `alias` values across lines —
> that's expected (the alias is the customer-facing name per line).

**Total raw rows:** 294,927
**Distinct (customer, line, process, alias):** 1,842
**Customers covered:** 26
**Production lines covered:** 152
**Distinct processes:** 207
**Distinct aliases:** 822

## 1. All distinct processes (system-wide)

| Process | # rows |
|---|---:|
| `Assembly 1` | 11,287 |
| `FNI 1` | 9,771 |
| `Assembly 3` | 9,083 |
| `OBA 1` | 9,069 |
| `Packout 1` | 8,628 |
| `Assembly 2` | 8,308 |
| `Link 1` | 7,953 |
| `FVT 1` | 7,023 |
| `QC 1` | 5,692 |
| `FVT 2` | 5,203 |
| `Link 2` | 5,097 |
| `Label 1` | 4,776 |
| `Depanel 1` | 4,642 |
| `Assembly 5` | 4,590 |
| `Assembly 4` | 4,579 |
| `Wave 1` | 4,425 |
| `Touch Up 1` | 4,241 |
| `MI 1` | 4,106 |
| `Placement TOP 1` | 4,047 |
| `SCR TOP 1` | 4,032 |
| `AOI TOP 1` | 4,005 |
| `Solder 1` | 3,989 |
| `SPI TOP 1` | 3,959 |
| `Reflow TOP 1` | 3,955 |
| `AOI BOT 1` | 3,954 |
| `SCR BOT 1` | 3,913 |
| `Link 3` | 3,906 |
| `ICT 1` | 3,902 |
| `Placement BOT 1` | 3,863 |
| `SPI BOT 1` | 3,834 |
| `TSI 1` | 3,801 |
| `BSI 1` | 3,714 |
| `Reflow BOT 1` | 3,706 |
| `ICT 2` | 3,663 |
| `Press 1` | 3,475 |
| `XRAY 1` | 3,311 |
| `Assembly 6` | 3,234 |
| `THI 1` | 3,198 |
| `FNI 2` | 3,185 |
| `Assembly 7` | 3,046 |
| `MI 2` | 3,027 |
| `Birth 1` | 2,952 |
| `QC 2` | 2,827 |
| `Test 1` | 2,735 |
| `Dispense TOP 1` | 2,477 |
| `Press 2` | 2,377 |
| `Handplace TOP 1` | 2,320 |
| `Assembly 8` | 2,318 |
| `Link 4` | 2,118 |
| `Hi-Pot 1` | 2,055 |
| `Assembly 10` | 1,996 |
| `Test 2` | 1,987 |
| `Test 3` | 1,970 |
| `Assembly 9` | 1,912 |
| `Wash 1` | 1,905 |
| `OBA 2` | 1,893 |
| `Handplace BOT 1` | 1,876 |
| `Program 1` | 1,870 |
| `QC 3` | 1,734 |
| `Touch Up 2` | 1,728 |
| `QC 4` | 1,577 |
| `FVT 3` | 1,548 |
| `Selective 1` | 1,545 |
| `Wave 2` | 1,516 |
| `Packout 2` | 1,228 |
| `FNI 3` | 1,215 |
| `QC 5` | 1,208 |
| `Leak Test 1` | 1,193 |
| `Solder 2` | 1,150 |
| `Dispense BOT 1` | 1,066 |
| `Oven 1` | 1,059 |
| `Wash 2` | 1,007 |
| `Wash 3` | 917 |
| `Link 5` | 899 |
| `Test 4` | 826 |
| `ICT 3` | 797 |
| `QC 6` | 776 |
| `Mask 1` | 764 |
| `Curing 1` | 762 |
| `ESS 1` | 751 |
| `Potting 1` | 713 |
| `CC Cure 1` | 689 |
| `CC QC 2` | 680 |
| `CC Oven 1` | 680 |
| `CC QC 1` | 680 |
| `Wash 4` | 655 |
| `CC Cure 2` | 652 |
| `CC Spray 2` | 650 |
| `CC Spray 1` | 650 |
| `Bonding 1` | 649 |
| `CC QC 4` | 649 |
| `CC QC 3` | 649 |
| `De-Mask 2` | 619 |
| `De-Mask 1` | 619 |
| `VMI 1` | 595 |
| `Oven 2` | 555 |
| `Link 6` | 531 |
| `Auto Insert 1` | 500 |
| `Oven 3` | 474 |
| `Burn-In 1` | 440 |
| `Curing 2` | 383 |
| `Placement TOP 2` | 379 |
| `Label 2` | 374 |
| `AOI BOT 2` | 366 |
| `AOI TOP 2` | 366 |
| `Prep 1` | 359 |
| `CC Oven 2` | 348 |
| `Mask 2` | 347 |
| `Dispense 1` | 343 |
| `Wash 8` | 301 |
| `Wash 5` | 301 |
| `CC Cure 4` | 301 |
| `CC Cure 3` | 301 |
| `Bonding 2` | 301 |
| `CC Touch Up 2` | 301 |
| `Wash 7` | 301 |
| `CC Touch Up 1` | 301 |
| `Curing 4` | 301 |
| `Curing 3` | 301 |
| `Solder 3` | 301 |
| `Wash 6` | 301 |
| `Assembly 11` | 280 |
| `Assembly 12` | 280 |
| `Assembly 13` | 271 |
| `Assembly 14` | 268 |
| `Oven 4` | 252 |
| `QC 7` | 232 |
| `QC 8` | 232 |
| `Test 6` | 207 |
| `Assembly 15` | 200 |
| `Assembly 16` | 200 |
| `Assembly 17` | 196 |
| `THI 2` | 196 |
| `Assembly 19` | 194 |
| `Assembly 22` | 194 |
| `Assembly 20` | 194 |
| `Assembly 21` | 194 |
| `Assembly 18` | 194 |
| `VMI 2` | 185 |
| `VMI 3` | 178 |
| `Assembly 24` | 176 |
| `Assembly 26` | 176 |
| `Assembly 31` | 176 |
| `Assembly 27` | 176 |
| `Assembly 34` | 176 |
| `Assembly 33` | 176 |
| `Assembly 32` | 176 |
| `Assembly 23` | 176 |
| `Assembly 35` | 173 |
| `Assembly 36` | 173 |
| `FVT 4` | 171 |
| `Test 5` | 169 |
| `FVT 5` | 169 |
| `Load 1` | 168 |
| `FVT 6` | 167 |
| `Test 8` | 155 |
| `Test 7` | 155 |
| `VMI 4` | 127 |
| `VMI 5` | 125 |
| `Test 9` | 117 |
| `OBA 3` | 110 |
| `AVI 1` | 104 |
| `VMI 6` | 104 |
| `Assembly 39` | 104 |
| `Assembly 38` | 104 |
| `Assembly 37` | 104 |
| `Program 2` | 101 |
| `MI 3` | 99 |
| `Assembly 30` | 97 |
| `Assembly 29` | 97 |
| `Assembly 28` | 97 |
| `Assembly 25` | 97 |
| `Press 3` | 95 |
| `Test 13` | 69 |
| `Test 15` | 69 |
| `Test 12` | 69 |
| `Test 14` | 69 |
| `XRAY 2` | 62 |
| `Test 10` | 58 |
| `Test 16` | 56 |
| `Test 17` | 56 |
| `Test 11` | 53 |
| `Cut 1` | 49 |
| `Weld 1` | 45 |
| `Ultrasonic 1` | 39 |
| `Weld 2` | 39 |
| `AOI 1` | 26 |
| `Assembly 40` | 25 |
| `XRAY 3` | 20 |
| `THI 3` | 17 |
| `FVT 7` | 15 |
| `Progression 1` | 14 |
| `Load 2` | 13 |
| `Charging 1` | 13 |
| `FVT 10` | 8 |
| `FVT 9` | 8 |
| `FVT 8` | 8 |
| `Link 7` | 8 |
| `Dispense 2` | 6 |
| `Depanel 2` | 5 |
| `Dispense 3` | 3 |
| `Dispense 4` | 3 |
| `Link 10` | 3 |
| `Link 8` | 3 |
| `Link 9` | 3 |
| `Reflow TOP 2` | 3 |
| `Program 3` | 1 |

## 2. All distinct aliases (system-wide)

| Alias | # rows |
|---|---:|
| `(no alias)` | 13,953 |
| `FVT 1` | 4,395 |
| `PACKOUT 1` | 4,307 |
| `OBA 1` | 3,936 |
| `FNI 1` | 3,911 |
| `MIT 1` | 3,679 |
| `MA 1` | 3,323 |
| `FVT 2` | 3,142 |
| `MA 3` | 2,827 |
| `HFNI 1` | 2,635 |
| `C WAVET 1` | 2,517 |
| `ROUTER 1` | 2,433 |
| `PWTU 1` | 2,415 |
| `HLA 2` | 2,393 |
| `HLA 1` | 2,393 |
| `M SOLDER 1` | 2,387 |
| `ICT 1` | 2,385 |
| `PRESS FIT 1` | 2,361 |
| `PACKOUT` | 2,067 |
| `BIRTH 1 - BIRTH` | 1,929 |
| `BIRTH 1` | 1,899 |
| `SMTB 1` | 1,887 |
| `SMTT 1` | 1,874 |
| `MA 2` | 1,873 |
| `TSI 1 - TSI` | 1,859 |
| `AOIB 1` | 1,857 |
| `REFLOWT 1` | 1,853 |
| `AOIT 1` | 1,851 |
| `SCRT 1` | 1,845 |
| `SCRB 1` | 1,837 |
| `SPIT 1 - SPI TOP` | 1,823 |
| `SCRT 1 - SCRT01` | 1,822 |
| `AOIT 1 - AOI TOP` | 1,789 |
| `REFLOWB 1` | 1,787 |
| `SMTT 1 - SMTT01` | 1,787 |
| `SPIB 1` | 1,767 |
| `BSI 1 - BSI` | 1,755 |
| `REFLOWT 1 - REFLOW SOLDERING TOP` | 1,741 |
| `SCRB 1 - SCRB01` | 1,666 |
| `SPIB 1 - SPI BTM` | 1,661 |
| `BSI 1` | 1,649 |
| `TSI 1` | 1,641 |
| `AOIB 1 - AOI BTM` | 1,628 |
| `XRAY 1` | 1,625 |
| `SMTB 1 - SMTB01` | 1,624 |
| `REFLOWB 1 - REFLOW SOLDERING BTM` | 1,564 |
| `HANDPLACET 1` | 1,544 |
| `PACKOUT 1 - PACKOUT` | 1,428 |
| `SPIT 1` | 1,407 |
| `TSTH 1 - TSTH` | 1,384 |
| `XRAY 1 - XRAY` | 1,379 |
| `FRONT MA 1` | 1,346 |
| `FNI 1 - FNI` | 1,282 |
| `OBA 1 - OQA` | 1,266 |
| `PRESS FITB 1` | 1,260 |
| `FPROBE 1` | 1,246 |
| `HLA 3` | 1,236 |
| `FNI` | 1,229 |
| `S WAVET 1` | 1,222 |
| `ICT 1 - ICT` | 1,218 |
| `HLA 4` | 1,214 |
| `TSTH 1` | 1,205 |
| `FRONT MA 2` | 1,185 |
| `HANDPLACEB 1` | 1,163 |
| `PROG (EEPROM) 1` | 1,154 |
| `FNI 3` | 1,154 |
| `MA 5` | 1,154 |
| `MA 8` | 1,154 |
| `ICT 2` | 1,154 |
| `PRESS FIT 2` | 1,154 |
| `MA 10` | 1,154 |
| `FRONT MA 3` | 1,154 |
| `TEST (COM LEAK) 1` | 1,154 |
| `MA 4` | 1,154 |
| `MA 9` | 1,154 |
| `OBA` | 1,130 |
| `BACK MA 1 - BACK MECH ASSY 1` | 1,089 |
| `HOBA 1` | 985 |
| `BIRTH 1 - LABELING` | 917 |
| `GLUET 1 - GLUET01` | 913 |
| `FVT 1 - FVT` | 892 |
| `BIRTH (HLA) 1` | 867 |
| `INSP VIP (HLA) 1` | 867 |
| `INSP VIP (HLA) 2` | 814 |
| `INSP (HLA) 1` | 812 |
| `INSP VIP (HLA) 3` | 811 |
| `FNI 1 - HFNI` | 801 |
| `PWTU 1 - PWTU BTM` | 756 |
| `V LINK 1` | 751 |
| `HIPOT 1 - HIPOT` | 746 |
| `CWAVET 1 - CONVENTIONAL WAVE SOLDERING TOP` | 734 |
| `PACKOUT - PACKOUT` | 725 |
| `WASH 1 - WASH 1 LINK` | 724 |
| `HI-PORT` | 719 |
| `MA 1 - SMART TORQUE 1` | 716 |
| `CWAVE 1 - CONVENTIONAL WAVE SOLDERING BTM` | 713 |
| `POST WASH INSP 1 - Post Wash 1 Insp` | 713 |
| `POT 1 - POTTING` | 713 |
| `MI 1 - MI TOP 1` | 713 |
| `MA 2 - HLA MECH ASSY 2` | 713 |
| `MA 2 - SMART TORQUE 2` | 713 |
| `PACKOUT 1 - HLAPACKOUT LINK` | 713 |
| `PACKOUT 1 - PACKOUT LINK` | 713 |
| `MI 1 - MI BTM LINK` | 713 |
| `MA 2 - HLA 2 LINK` | 713 |
| `MI 1 - MI BTM 1` | 713 |
| `BACK MA 1 - BACK MA 1 LINK` | 713 |
| `PRESS FIT 1 - PRESS FIT 1` | 713 |
| `PWTU 1 - PWTU BTM LINK` | 713 |
| `MA 1 - HLA 1 LINK` | 713 |
| `SYSTEM TEST 2 - SYSTEM TEST 1` | 713 |
| `SYSTEM TEST 1 - SYSTEM TEST` | 713 |
| `WASH 1 - Wash1` | 713 |
| `HPLACEB 1 - MANUAL ONSERT BTM` | 713 |
| `HPLACET 1 - MANUAL ONSERT TOP` | 713 |
| `M SOLDER 2 - M.SOLDERING 2` | 713 |
| `FVT 3 - FVT 2` | 713 |
| `PWTU 1 - PWTU TOP` | 713 |
| `M SOLDER 1 - M.SOLDER 1 LINK` | 713 |
| `GLUEB 1 - GLUEB01` | 713 |
| `SYSTEM TEST 3 - SYSTEM TEST 2` | 713 |
| `M SOLDER 2 - M.SOLDER 2 LINK` | 713 |
| `HFNI 1 - HFNI VIP` | 713 |
| `PWTU 1 - PWTU TOP LINK` | 713 |
| `PRE TEST 1 - BIRTH_01` | 713 |
| `M SOLDER 1 - M.SOLDERING 1` | 713 |
| `MA 1 - HLA MECH ASSY 1` | 713 |
| `FVT 2 - FVT 1` | 713 |
| `MA INSP 1 - HLA MAI 1` | 713 |
| `MI 1 - MI TOP LINK` | 713 |
| `MA 3 - HLA 3 LINK` | 713 |
| `MA 2 - Mech Assy2` | 713 |
| `MA 3 - SMART TORQUE 3` | 713 |
| `DEPANEL 1 - DEPANELING` | 713 |
| `MA 3 - Mech Assy3` | 713 |
| `MA 3 - HLA MECH ASSY 3` | 713 |
| `FPROBEB 1 - FLYING PROBE BTM` | 713 |
| `FPROBET 1 - FLYING PROBE TOP` | 713 |
| `OBA 1 - HOQA VIP` | 713 |
| `CWAVE 1 - CONVENTIONAL WAVE SOLDERING TOP` | 713 |
| `MA INSP 2 - HLA MAI 2` | 713 |
| `OBA 1 - HOQA` | 713 |
| `CWAVEB 1 - CONVENTIONAL WAVE SOLDERING BTM` | 712 |
| `MIT 1 - MI TOP LINK` | 699 |
| `PWTUT 1 - PWTU TOP` | 699 |
| `BAKE 1 - BAKING PCBA` | 699 |
| `ROUTER 1 - Router` | 696 |
| `MIT 1 - MI TOP 1` | 660 |
| `INSP (HLA) 2` | 526 |
| `BAKE 1` | 512 |
| `INSP (HLA) 3` | 504 |
| `HLA 6` | 485 |
| `HLA 5` | 485 |
| `HLA 7` | 485 |
| `MIB 1 - MI BTM 1` | 474 |
| `FRONT MA 1 - FRONT MECH ASSY 1` | 446 |
| `HLA 8` | 424 |
| `HLA 10` | 424 |
| `HLA 9` | 424 |
| `HIPOT 1` | 422 |
| `MIB 1 - MI BTM LINK` | 421 |
| `WASH 1 - WASH 1` | 417 |
| `PWTUB 1 - PWTU BTM` | 414 |
| `WASH 2 - WASH 2` | 413 |
| `MSOLDER 1 - M.SOLDERING` | 404 |
| `FVT 1 - FVT 1` | 395 |
| `FVT` | 380 |
| `SMTT 2` | 379 |
| `PRE WASH 1 - WASH 1 LINK` | 368 |
| `PRE AOIB 1` | 366 |
| `SPI TOP 1` | 366 |
| `PRE AOIT 1` | 366 |
| `WASH 3 - WASH 3` | 361 |
| `MA (SUB)` | 360 |
| `FVT1 / FVT 4` | 360 |
| `FVT 2 / FVT 3` | 360 |
| `CURING` | 360 |
| `VMI` | 360 |
| `WASH BASIN MA` | 359 |
| `EBOX MA` | 359 |
| `BURN IN` | 359 |
| `EBOX PREP` | 359 |
| `MA INSP` | 359 |
| `EBOX CRIMP` | 359 |
| `TEST (NL COMPRO) 1` | 356 |
| `PROG (NL BRD) 1` | 356 |
| `LABEL (COMPRO) 1` | 356 |
| `TEST (NL SNC) 1` | 356 |
| `TEST (NL BEST ) 1` | 356 |
| `TEST (NL CIT) 1` | 356 |
| `PRE WASH 2 - WASH 2 LINK` | 355 |
| `PRE WASH 3 - WASH 3 LINK` | 355 |
| `Birth 1` | 355 |
| `ESS 1 - ESS` | 350 |
| `TEST (IONIC) 1 - IONIC TEST 1` | 350 |
| `ACOATT 1 - AUTO COATING TOP` | 349 |
| `FNI  2 - FNI 2 VIP` | 349 |
| `ACOATB 1 - AUTO COATING BTM` | 349 |
| `OBA 2 - OQA 2 VIP` | 349 |
| `FNI 1 - FNI 1 VIP` | 349 |
| `OBA 1 - OQA 1 VIP` | 349 |
| `CUREB 1 - CURING BTM` | 348 |
| `BAKE 3 - BAKING PCBA WASH 3` | 348 |
| `CURET 1 - CURING TOP` | 348 |
| `PMI 1 - PMI` | 348 |
| `POST COAT INSPT 1 - POST COATING INSP TOP` | 348 |
| `POST COAT INSPB 1 - POST COATING INSP BTM` | 348 |
| `BACK MA 2 - BACK MECH ASSY 2` | 348 |
| `BACK MA 1 - SMART TORQUE 2` | 348 |
| `BACK MA 2 - SMART TORQUE 3` | 348 |
| `BAKE 2 - BAKING PCBA WASH 2` | 348 |
| `BAKE 1 - BAKING PCBA WASH 1` | 348 |
| `POST WASH INSP 3 - Post Wash 3 Insp` | 348 |
| `BACK MA 1 - MA LINK` | 348 |
| `BAKE 2 - PCB Baking` | 348 |
| `BOND 1 - BONDING 1` | 348 |
| `BACK MA 3 - BACK MECH ASSY 3` | 348 |
| `POST WASH INSP 2 - Post Wash 2 Insp` | 348 |
| `BACK MA 4 - SMART TORQUE 5` | 348 |
| `BACK MA 3 - SMART TORQUE 4` | 348 |
| `PRE WASH 4 - WASH 4 LINK` | 348 |
| `BACK MA 4 - BACK MECH ASSY 4` | 348 |
| `WASH 4 - WASH 4` | 348 |
| `PRE COAT INSPT 1 - PRE COATING INSP TOP` | 347 |
| `MASKT 1 - MASKING TOP 1` | 347 |
| `MASKB 1 - MASKING BTM 1` | 347 |
| `PRE COAT INSPB 1 - PRE COATING INSP BTM` | 347 |
| `FRONT MA 1 - SMART TORQUE 1` | 347 |
| `FRONT MA 1 - MAI 1` | 347 |
| `POST WASH 1 - Post Wash 1 Insp` | 332 |
| `POST WASH INSP 4 - Post Wash 4 Insp` | 332 |
| `FVT 1 - FVT 2` | 331 |
| `LINK AOP - AOP LINK` | 330 |
| `AI 1 - AUTO INSERT 1` | 321 |
| `VMI 1` | 319 |
| `DEMASKB 1 - UNMASKING BTM 1` | 318 |
| `DEMASKT 1 - UNMASKING TOP 1` | 318 |
| `AI INSP 1 - AI Insp` | 311 |
| `GLUET 1 - Glue GLUET01` | 309 |
| `GLUEB 1 - Glue GLUEB01` | 305 |
| `ROUTER 1 - DEPANELING` | 305 |
| `CHEMASK 1 - PRE MI` | 302 |
| `EPTSB 1 - LINK EPTS BTM` | 301 |
| `WASH (CHEM) 4 - WASH WASH 4` | 301 |
| `BIRTH 1 - LABEL` | 301 |
| `COATB 1 - COATING Coating Bot` | 301 |
| `ESS 1 - FVT ESS` | 301 |
| `CURE (EPOXY) 1 - CURING EPOXY CURING 1` | 301 |
| `CURE (EPOXY) 2 - CURING EPOXY CURING 2` | 301 |
| `CURE 1 - CURING CURING` | 301 |
| `C WAVE 1 - WAVE WAVE CONVENTIONAL` | 301 |
| `EPTST 1 - LINK EPTS TOP` | 301 |
| `OBA VIP 2 - QC OQA2_VIP` | 301 |
| `SPIB 1 - SPI BTM 1` | 301 |
| `SPIT 1 - SMT SPI TOP` | 301 |
| `STAGEB 1 - Assemble Staging Bot` | 301 |
| `STAGET 1 - Assemble Stanging Top` | 301 |
| `ICT 1 - ICT ICT` | 301 |
| `SMTB 1 - SMT SMTB01` | 301 |
| `SMTT 1 - SMT SMTT01` | 301 |
| `WASH 1 - WASH Aqueous WASH 1` | 301 |
| `WASH 2 - LINK WASH 2 LINK` | 301 |
| `MI 2 - Assemble MI_2` | 301 |
| `MI 2 - LINK MI2` | 301 |
| `MI 1 - Assemble MI_1` | 301 |
| `MI 1 - LINK MI1` | 301 |
| `MASK 1 - Assemble MASKING 1 BOT & TOP` | 301 |
| `OBA VIP 1 - QC OQA1_VIP` | 301 |
| `XRAY 1 - XRAY XRAY` | 301 |
| `WASH (CHEM) 1 - WASH WASH` | 301 |
| `WASH (CHEM) 2 - WASH WASH 2` | 301 |
| `WASH (CHEM) 3 - WASH WASH 3` | 301 |
| `AOIT 1 - AOI AOI TOP` | 301 |
| `PRE PWTU 1 - QC Pre PWTU 1` | 301 |
| `TSI 1 - QC TSI` | 301 |
| `MA 2 - SMART TORQUE SMART TORQUE 2` | 301 |
| `FNI VIP 2 - QC FNI2_VIP` | 301 |
| `FNI VIP 1 - QC FNI1_VIP` | 301 |
| `MA 2 - Assemble Mech Assy2` | 301 |
| `TU (COATT1) 1 - COATING TOUCH COAT` | 301 |
| `PRE PWTU 2 - QC Pre PWTU 2` | 301 |
| `PRE WASH 3 - WASH Pre-Wash 3` | 301 |
| `PRE WASH 4 - WASH Pre-Wash 4` | 301 |
| `PRE MI (SCREW) 1 - Manual PRE-MI` | 301 |
| `INSPB (POST COAT) 1 - QC POST COATING INSP BTM` | 301 |
| `INSPB (PRE COAT) 1 - QC PRE COATING INSP BTM` | 301 |
| `TSTH 1 - QC TSTH` | 301 |
| `PRE WASH 1 - WASH Pre-Wash 1` | 301 |
| `TU (COATB1) 1 - Assemble Coating Touch up` | 301 |
| `ROUTER 1 - Router Router` | 301 |
| `INSPT (PRE COAT) 1 - QC PRE COATING INSP TOP` | 301 |
| `SCRB 1 - SCR SCRB01` | 301 |
| `INSP (WASH4) 1 - QC Post Wash 4 Insp` | 301 |
| `SCRT 1 - SCR SCRT01` | 301 |
| `S WAVE 1 - WAVE SELECTIVE WAVE` | 301 |
| `FVT 1 - FVT FVT1` | 301 |
| `FPROBE 1 - AUTOTEST TAKAYA_AUTO` | 301 |
| `MA 1 - SMART TORQUE SMART TORQUE 1` | 301 |
| `MA 1 - Assemble Mech Assy1` | 301 |
| `FVT 3 - FVT FVT3` | 301 |
| `FVT 2 - FVT FVT2` | 301 |
| `REFLOWB 1 - Oven REFLOW SOLDERING BTM` | 301 |
| `INSPT (POST COAT) 1 - QC POST COATING INSP TOP` | 301 |
| `INSP (WASH1) 1 - QC POST WASH 1 INSPECTION` | 301 |
| `PRE WASH 2 - WASH Pre-Wash 2` | 301 |
| `PWTU 2 - QC PWTU2` | 301 |
| `PWTU 1 - QC PWTU1` | 301 |
| `REFLOWT 1 - Oven REFLOW SOLDERING TOP` | 301 |
| `TEST (IONIC) 3 - Manual Test IONIC TEST 3` | 301 |
| `TEST (BSCAN) 2 - AUTOTEST BOUNDARY SCAN 2` | 301 |
| `TEST (BSCAN) 1 - AUTOTEST BOUNDARY SCAN 1` | 301 |
| `TEST (IONIC) 1 - Manual Test IONIC TEST 1` | 301 |
| `TEST (IONIC) 4 - Manual Test IONIC TEST 4` | 301 |
| `M SOLDER 1 - Assemble Manual Soldering 1 # 1` | 301 |
| `M SOLDER 2 - Assemble Manual Soldering 1 # 2` | 301 |
| `INSP (WASH2) 1 - QC POST WASH 2 INSPECTION` | 301 |
| `INSP (WASH3) 1 - QC POST WASH 3 INSPECTION` | 301 |
| `M SOLDER 3 - Assemble Manual Soldering 1 # 3` | 301 |
| `PACKOUT  - PACKOUT PACKOUT` | 301 |
| `AOIB 1 - AOI AOI BTM` | 301 |
| `TEST (IONIC) 2 - Manual Test IONIC TEST 2` | 301 |
| `CURE 2 - CURING CURING 2` | 301 |
| `CUREB 1 - CURING Curing Bot` | 301 |
| `COATT 1 - COATING Coating Top` | 301 |
| `CURET 1 - CURING CURING TOP` | 301 |
| `BOND 2  - Assemble BONDING 2` | 301 |
| `BAKE 1 - BAKING BAKING1` | 301 |
| `WASH 3 - WASH Aqueous WASH 3` | 301 |
| `BOND 1 - Assemble BONDING 1` | 301 |
| `WASH 4 - LINK WASH 4 LINK` | 301 |
| `WASH 4 - WASH Aqueous WASH 4` | 301 |
| `WASH 3 - LINK WASH 3 LINK` | 301 |
| `WASH 2 - WASH Aqueous WASH 2` | 301 |
| `BSI 1 - QC BSI` | 301 |
| `UNMASKB 1 - Assemble DE-Masking Bot` | 301 |
| `UNMASKT 1 - Assemble DE- Masking Top` | 301 |
| `WASH 1 - LINK WASH 1 LINK` | 301 |
| `PACKOUT  - PACKOUT` | 283 |
| `BAKE 4 - BAKING PCBA WASH 4` | 252 |
| `MA 2.1` | 252 |
| `LINK (COMBO) 1` | 249 |
| `PACKOUT - PACKOUT LINK` | 243 |
| `FNI 1 - FNI VIP` | 242 |
| `OBA 1 - OQA VIP` | 239 |
| `PMI 1` | 234 |
| `PROG 1 - PROGRAMMING` | 231 |
| `POST WASH 1 - POST WASH 1 INSP` | 229 |
| `PWTU 1 - PWTU` | 227 |
| `MA 2.2` | 215 |
| `LINK (AOP) 1` | 204 |
| `BACK MA 1` | 199 |
| `WASH 1 - WASH` | 195 |
| `WASH 3` | 194 |
| `PALLETIZING 1` | 194 |
| `WASH 1 - WASH LINK` | 192 |
| `OBA VIP 1` | 181 |
| `INSP (AI) 1` | 179 |
| `PRESS FIT (MEP) 1` | 179 |
| `AI 1` | 179 |
| `MA (TORQUE) 1` | 179 |
| `PRE MI 1` | 179 |
| `PRE FVT INSP (OPTIC) 1` | 177 |
| `FNI VIP 1` | 176 |
| `TSTHT 1` | 171 |
| `POST WASH 2 - POST WASH 2 INSP` | 170 |
| `WASH 2 - WASH 1` | 168 |
| `WASH 2 - WASH 1 LINK` | 167 |
| `MI 1 - MI_1` | 166 |
| `PWTU 1 - PWTU LINK` | 166 |
| `CWAVE 1 - WAVE CONVENTIONAL` | 166 |
| `WASH 1` | 166 |
| `PUNCH 1` | 165 |
| `FNI (TMA) 1` | 165 |
| `LOADB 1` | 165 |
| `V LINK (TMA) 1` | 165 |
| `HLA (TMA) 3` | 165 |
| `PACKOUT (TMA) 1` | 158 |
| `OBA (TMA) 1` | 158 |
| `FVT 1 - FVT 3` | 155 |
| `FVT 1 - FVT 4` | 152 |
| `VMI (OPT 30)` | 151 |
| `MA (OPT 30)` | 151 |
| `MA (OPT 20)` | 151 |
| `FA` | 151 |
| `VMI (OPT 10)` | 151 |
| `VMI (OPT 20)` | 151 |
| `MA (OPT 10)` | 151 |
| `TEST (PB)` | 151 |
| `FQC` | 151 |
| `FVT 1 - FVT 5` | 151 |
| `MA (SUB 10)` | 138 |
| `MA (SUB 30)` | 138 |
| `MA (SUB 20)` | 138 |
| `PFIT 1 - Press Fit` | 135 |
| `MA 1 - BACK MECH ASSY 1` | 133 |
| `PALLETIZING (TMA) 1` | 127 |
| `BAKE 3` | 126 |
| `BAKE 2` | 126 |
| `OCV 1` | 125 |
| `FVT (SHORT) 2` | 122 |
| `LABEL (BE) 1` | 122 |
| `FVT (CELL) 4` | 122 |
| `FST (TMA) 1` | 121 |
| `HIPOT (TMA) 1` | 121 |
| `PMI VIP 1` | 121 |
| `LINK (MI) 1` | 118 |
| `OBA1` | 118 |
| `FNI (AOP) 1` | 118 |
| `AOIB (BE) 1` | 118 |
| `FVT (FUSE) 3` | 118 |
| `MASKB 1` | 116 |
| `MA (OPT 40)` | 113 |
| `VMI (OPT 40)` | 113 |
| `BACK MA 5` | 113 |
| `FPROBE 1 - FLYING PROBE` | 112 |
| `MAI 3` | 109 |
| `SUB MA 1` | 109 |
| `SUB MA 2` | 109 |
| `BMA 2` | 109 |
| `FVT (DCEO) 1` | 109 |
| `FVT (BER) 1` | 109 |
| `INSP (OPTIC) 4` | 109 |
| `INSP (OPTIC) 3` | 109 |
| `PRE MA 1` | 109 |
| `FVT (OFCT) 1` | 107 |
| `MSOLDER 1 - M.SOLDERING 1` | 104 |
| `MA (OPT 50)` | 104 |
| `MA (OPT 60)` | 104 |
| `VMI (OPT 50)` | 104 |
| `VMI (OPT 60)` | 104 |
| `FPROBE 1 - Flying probe` | 102 |
| `PROG (QNX) 1 - QNX PROGRAMMING` | 101 |
| `Loopback 1` | 101 |
| `UWASH 1 - ULTROSONIC WASH 1` | 100 |
| `MA (SUB 50)` | 100 |
| `ROUTER 1 - Depanel` | 100 |
| `MA (SUB 60)` | 100 |
| `ESS 1` | 100 |
| `MA (SUB 40)` | 100 |
| `POST XRAY 1 - XRAY` | 100 |
| `GLUET 1 - GLUE TOP` | 100 |
| `OCV (TMA) 1` | 96 |
| `PACK VER 1` | 93 |
| `WASH 2` | 93 |
| `FVT 3` | 91 |
| `HLA 1 - HLA BIRTH` | 88 |
| `HLA 1 - HLA 2 LINK` | 83 |
| `OBA 1 - HOBA` | 82 |
| `HLA 1 - HLA MAI 2` | 82 |
| `CURE 1` | 82 |
| `BE BIRTH 1` | 81 |
| `HLA 1 - HLA MECH ASSY 2` | 81 |
| `BURN IN 1` | 81 |
| `HLA 1 - HLA MECH ASSY 1` | 80 |
| `MA 2.3` | 78 |
| `PMI 2` | 78 |
| `TEST 8` | 78 |
| `TEST 6` | 78 |
| `TEST 7` | 78 |
| `MA 2.5` | 78 |
| `HLA 1 - HLA LINK` | 78 |
| `MA 2.4` | 78 |
| `BACK MA 2` | 76 |
| `BIRTH (SUB HLA) 1` | 76 |
| `HLA BIRTH 1` | 75 |
| `LINK (OPTIC) 1` | 72 |
| `CLEAN (PLASMA) 1` | 72 |
| `MA 1 - LINK 1` | 72 |
| `OFF CLEAN (EEN) 1` | 72 |
| `BAKE (EEN) 1` | 72 |
| `PRESS FITT 1` | 69 |
| `TEST (RAJ LEAK) 1` | 68 |
| `TEST (RAJ CIT) 1` | 68 |
| `TEST (RAJ SNC) 1` | 68 |
| `HLA 13` | 68 |
| `HLA 11` | 68 |
| `HLA 12` | 68 |
| `PROG (RAJ BOARD) 1` | 68 |
| `HLA 14` | 68 |
| `TEST (RAJS ATS) 1` | 68 |
| `TEST (RAJS BEST) 1` | 68 |
| `TEST (RAJ WIRELESS) 1` | 68 |
| `MSOLDER 1 - M.SOLDER 1 LINK` | 67 |
| `BACK MA 4` | 67 |
| `HLA 1 - HLA MECH ASSY` | 65 |
| `LINK (FRONT MA) 1` | 65 |
| `TSTHB 1` | 63 |
| `CHEMASK 1` | 63 |
| `HPLACET 1` | 63 |
| `MIB 1` | 63 |
| `SPLICE (OPTIC) 1` | 63 |
| `POST FVT INSP (OPTIC) 1` | 63 |
| `VMI 1 - VMI` | 63 |
| `XRAY 2` | 62 |
| `XHFNI 1` | 61 |
| `INSP (HLA) 4` | 61 |
| `INSP VIP (HLA) 4` | 61 |
| `C WAVEB 1` | 61 |
| `PWTUB 1` | 61 |
| `POST UWASH 1 - POST WASH 3 INSP` | 60 |
| `LINK AOP - AOP FNI` | 58 |
| `SPB 1` | 58 |
| `SCB 1` | 58 |
| `TEST (C TUNE) 1 - FVT Ctune` | 57 |
| `MA 2 - BACK MECH ASSY 1` | 57 |
| `FRONT MA 2 - FRONT MECH ASSY 2` | 57 |
| `ASOLDER 1 - ROBOTIC SOLDERING BTM 1` | 57 |
| `TEST (RF) 1 - FVT RF` | 57 |
| `TEST (NON RF) 1 - FVT Non RF` | 57 |
| `BACK MA 8` | 56 |
| `BIRTH 1  - BIRTH` | 56 |
| `BACK MA 6` | 56 |
| `TEST 9` | 56 |
| `HLA 1 - HLA 1 LINK` | 54 |
| `ROUTER 1  - DEPANELING` | 54 |
| `SMTB 1  - SMTT01` | 54 |
| `AOIB 1  - AOI TOP` | 54 |
| `SCRB 1  - SCRT01` | 54 |
| `XRAY 1  - XRAY 1` | 54 |
| `HLA 1 - HLA MAI 1` | 52 |
| `UWASH 1 - WASH 2 LINK` | 52 |
| `SPIB 1  - SPI TOP` | 52 |
| `SMTB 1  - SMTB01` | 51 |
| `REFLOWB 1  - REFLOW SOLDERING BTM` | 51 |
| `SCRB 1  - SCRB01` | 51 |
| `BACK MA 3` | 50 |
| `AOIB 1  - AOI BTM` | 50 |
| `AVI 1` | 50 |
| `MA 2.6` | 50 |
| `TEST (SMART IMAGE)` | 49 |
| `VER (FIBER) 1` | 47 |
| `REFLOWB 1  - REFLOW SOLDERING TOP` | 47 |
| `SPIB 1  - SPI BTM` | 47 |
| `MAI 2` | 46 |
| `PRE MA 2` | 46 |
| `FNI 1 - FNI LINK` | 46 |
| `INSP (OPTIC) 1` | 46 |
| `LABEL (LASER) 1` | 46 |
| `ASOLDERB (HOTBAR) 1` | 45 |
| `GLUEB 1 - GLUE DISPENSING BTM` | 43 |
| `CUT 1 - CUTTING` | 43 |
| `TSTH 1- TSTH` | 43 |
| `MSOLDER (HOTB) 1 - M. SOLDERING 1` | 43 |
| `LABEL 1 - BIRTH` | 41 |
| `MA 1 - Dep OPT 10` | 39 |
| `PWTUT 1 - PWTU TOP LINK` | 39 |
| `MA 1 - Dep OPT 30` | 39 |
| `MA 1 - Dep OPT 20` | 39 |
| `FVT 1 - Dep FVT` | 39 |
| `TACK WELD 1 - TACK WELDING` | 39 |
| `FQC 1 - Dep FQC 10` | 39 |
| `MA 1 - Dep OPT 40` | 39 |
| `FMA 1 - Dep FA 10` | 39 |
| `PDT 1 - Dep PD` | 39 |
| `TWEAK TEST 1 - TWEAKING` | 39 |
| `WELD INSP - WELDMENT INSPECTION` | 39 |
| `ORBITAL WELD 1 - ORBITAL WELD` | 39 |
| `PACKOUT 1 - Bagging10` | 39 |
| `PACKOUT 1 - Dep Bagging` | 39 |
| `MIT 1 - MI_Top` | 39 |
| `SUB MA 1 - Dep Pallet assy 10` | 39 |
| `FNI 1 - Dep FNI 10` | 39 |
| `SUB MA 1 - Dep Pallet assy 20` | 39 |
| `LEAK TEST 1 - LEAK TEST` | 39 |
| `SUB MA 1 - Dep Pallet assy 40` | 39 |
| `SUB MA 1 - Dep Pallet assy 30` | 39 |
| `PWTUT 1` | 38 |
| `TEST (VERIF) 1 - TEST VERIFICATION` | 36 |
| `MSOLDER 1 - M.SOLDERING 2` | 35 |
| `MSOLDER 1 - MANUAL SOLDERING 2 LINK` | 35 |
| `TEST 1` | 35 |
| `TSTHT 1 - TSTH TOP` | 34 |
| `AVI 1 - AVI` | 33 |
| `PRE INSERTT 1` | 33 |
| `QC 1` | 33 |
| `FPROBEB 1` | 31 |
| `QC 2` | 31 |
| `UF CURE 1` | 31 |
| `HLA MECH ASSY 1` | 30 |
| `MSOLDER 1` | 30 |
| `FVT, FIRMWARE,NIC` | 30 |
| `PROVISIONING` | 30 |
| `HFNI 2` | 30 |
| `HIPOT` | 30 |
| `FVT 2 - FVT1` | 29 |
| `FST 1` | 29 |
| `FNI 1 - VMI` | 28 |
| `FNI 1 - VMIO` | 28 |
| `VMI 2` | 28 |
| `ASOLDERT (HOTBAR) 1` | 28 |
| `PACKOUT TRANSFER - PACKOUTTRANSFER` | 27 |
| `LOOPBACK 1` | 27 |
| `FPROBEB 1  - TAKAYA_B` | 27 |
| `OBA 1 - OBA` | 27 |
| `VMI 3` | 27 |
| `WASHT 1  - WASH TOP LINK` | 27 |
| `AOIBE 1` | 26 |
| `GLUEB 1` | 26 |
| `WASHT 1  - WASH TOP` | 25 |
| `MA 1 - MA-1` | 23 |
| `WASHB 1  - WASH BTM LINK` | 23 |
| `PACKOUT  - PACKOUT LINK` | 23 |
| `FNI 1 - FNI-1` | 23 |
| `MA 1 - LINK` | 23 |
| `FNI 1 - LED LIGHT ON VERIFICATION` | 23 |
| `HLA 1 - HLA MAI 3` | 23 |
| `MSOLDER 1 - MANUAL SOLDER 1` | 23 |
| `TEST 3` | 22 |
| `TEST 5` | 22 |
| `LINK 3` | 22 |
| `TEST (VERTICAL)` | 22 |
| `TEST 4` | 22 |
| `AOP FNI` | 21 |
| `VMI 5` | 21 |
| `WASHB 1 - WASH BTM` | 21 |
| `BACK MECH ASSY 2` | 21 |
| `BACK MECH ASSY 1` | 21 |
| `BIRTH ` | 21 |
| `BST` | 21 |
| `SMTT1` | 21 |
| `MAGIC RAY` | 21 |
| `MI TOP` | 21 |
| `MA 1 - BIRTH` | 21 |
| `PWTU` | 21 |
| `WAVE` | 21 |
| `LABEL 1 - LABELING` | 21 |
| `ROUTER` | 21 |
| `XRAY` | 21 |
| `ICT` | 21 |
| `FPROBET 1` | 20 |
| `WASH 1 - CHEMICAL WASH 1` | 20 |
| `XRAY 3` | 20 |
| `LMARKER 1 - LASER MARKER` | 20 |
| `CURE 1 - CURING` | 19 |
| `FPROBET 1  - TAKAYA_T` | 18 |
| `LINK (AOP) 2` | 18 |
| `FNI (AOP) 2` | 18 |
| `SUB MA 1 - HLA BIRTH` | 17 |
| `SUB MA 1 - HLA MAI 1` | 17 |
| `PACKOUT - Packout` | 17 |
| `HIPOT 1 - Hipot` | 17 |
| `SUB MA 2 - HLA MAI 2` | 17 |
| `SUB MA 2 - Sub Assembly 2` | 17 |
| `HLA 2 - HLA MAI 4` | 17 |
| `FVT 1 - Final Test` | 17 |
| `SUBT (LIGHT PIPE) 1` | 17 |
| `FQC 1 - OQA (FQC)` | 17 |
| `FVT 1 - FVT1` | 17 |
| `PWTUB 1 - PWTU BTM LINK` | 16 |
| `APFIT 1 - AUTO PRESS 1` | 16 |
| `TEST (IONIC) 1 - IONIC TEST` | 16 |
| `PACKOUT - Pack Verify` | 15 |
| `FA 1 - HLA Mech Assy 3 (FA)` | 15 |
| `FA 1 - HLA 5 LINK` | 15 |
| `HLA 2 - HLA 4 LINK` | 15 |
| `SUB MA 1 - Sub Assembly 1` | 15 |
| `HLA 1- HLA 3 LINK` | 15 |
| `HLA 1 - HLA Mech Assy 1` | 15 |
| `ICT 1 - ICT LINK` | 15 |
| `HLA 2 -HLA Mech Assy 2` | 15 |
| `SUB MA 1 - HLA 1 LINK` | 15 |
| `SUB MA 2 - HLA 2 LINK` | 15 |
| `VMI 4` | 14 |
| `OBA 3` | 14 |
| `OBA 2` | 14 |
| `PRGS 1` | 14 |
| `CHARGE (BATT) 1 - BATTERY LEVEL CHECK` | 13 |
| `POST WASH INSP 1 - POST WASH 1 INSP` | 13 |
| `OBA 1 - OQA1 INSPECTION` | 13 |
| `OBA 1 - OQA1 TEST` | 13 |
| `TEST 1 ` | 13 |
| `QC 1 - HLA LABEL INSPECTION` | 13 |
| `PACK 1 - packing` | 13 |
| `LOADT 1` | 13 |
| `TSTHB 1 - TSTH BTM` | 12 |
| `FVT 1 - PROGRAMMING` | 12 |
| `MA 1 - BACK MECH ASSY 2` | 12 |
| `FVT 2 - FVT 2` | 12 |
| `HLA INSP 1 - HLA 1 LINK` | 12 |
| `PRE HLA 1 - PRE ASSY 1` | 12 |
| `PRE INSERTB 1` | 11 |
| `PTR FVT 1 - FVT` | 11 |
| `MI 1` | 11 |
| `A PRESS FIT 1` | 11 |
| `MA 1/2 - BACK MECH ASSY 1` | 11 |
| `MIT 1  - MI TOP LINK` | 11 |
| `TSTH 1  - TSTH TOP` | 11 |
| `PTR FVT (TRIM & CAL) 1 - FVT TRIM AND CALIBRATION` | 11 |
| `MIT 1  - MI TOP 1` | 11 |
| `SUBB (LIGHT PIPE) 1` | 11 |
| `CURE 4` | 10 |
| `SBL MA 1 - Sub Assy 1` | 10 |
| `PFIT 1 - PRESSFIT` | 10 |
| `AI INSP  1 - AI INSPECTION` | 10 |
| `FVT (RF) 3 - FVT RF` | 10 |
| `FVT (BATTERY CHARGING) 4 - FVT 2` | 10 |
| `FVT (FUNTIONAL TEST) 2 - FVT (FUNTIONAL TEST)` | 10 |
| `QC 1 - HFNI OCR 1` | 10 |
| `LID MA 2 - Sub Assy 1` | 9 |
| `PWTUT 1  - PWTU TOP` | 9 |
| `MA 1/2 - BACK MECH ASSY 2` | 9 |
| `BSI (BE) 1` | 9 |
| `PRE COND 1` | 9 |
| `LID MA 3 - Sub Assy 1` | 9 |
| `LID MA 1 - Sub Assy 1` | 9 |
| `FVT 1 - UL1` | 9 |
| `TSTH 1  - TSTH1` | 8 |
| `HLA 5 - HLA 5 LINK` | 8 |
| `HLA 1 - HLA 4 LINK` | 8 |
| `BIRTH 2` | 8 |
| `HLA 1 - HLA MECH ASSY 4` | 8 |
| `FVT 1 - FVT 7` | 8 |
| `FVT 1 - FVT 10` | 8 |
| `PREP (OPTIC) 1` | 8 |
| `MSOLDER (OPTIC) 1` | 8 |
| `FVT 1 - FVT 6` | 8 |
| `FVT 1 - FVT 8` | 8 |
| `FVT 1 - FVT 9` | 8 |
| `S WAVE 1` | 8 |
| `HLA 1 - HLA MAI 4` | 8 |
| `HLA 1 - HLA MECH ASSY 3` | 8 |
| `HLA 1 - HLA 3 LINK` | 8 |
| `HLA 5 - HLA MECH ASSY 5` | 8 |
| `CURE 1 - REFLOW OVEN CURING TOP` | 7 |
| `POST WASH INSP 2 - POST WASH 2 INSP` | 7 |
| `POST UF INSP - POST UNDERFILL INSPECTION` | 7 |
| `WASH 2 - CHEMICAL WASH 2` | 7 |
| `MI 1 - MI LINK` | 7 |
| `UF 1 - UNDERFILL INSPECTION` | 7 |
| `UF 1 - UNDER FILL` | 7 |
| `MI 1 - MI 1` | 7 |
| `WASH 2 - WASH 2 LINK` | 7 |
| `LSOLDER 1 - LASER SOLDERING` | 6 |
| `BACK MA 2 - BACK MECH ASSY 1` | 6 |
| `LROUTER 1 - LASER DEPANELING` | 6 |
| `WASH 3 - WASH 3 LINK` | 6 |
| `TSTH 1 - CUTTING` | 6 |
| `BACK MA 2 - PMI` | 6 |
| `LWELD 1 - LASER WELDING 1` | 6 |
| `CWASH 4 - WASH 4 LINK` | 6 |
| `CWASH 4 - WASH 4` | 6 |
| `FVT (STACK) 1 - FVT 1` | 5 |
| `MA 3/4 - BACK MECH ASSY 3` | 5 |
| `MA 3/4 - BACK MA 4 LINK` | 5 |
| `MA 3/4 - BACK MECH ASSY 4` | 5 |
| `MA 1/2 - BACK MA 1 LINK` | 5 |
| `MA 3/4 - BACK MA 3 LINK` | 5 |
| `ASOLDER 1 - LINK` | 5 |
| `ASOLDER 1 - ROBOTIC SOLDERING 1` | 5 |
| `MA 1/2 - BACK MA 2 LINK` | 5 |
| `ROUTER 2` | 5 |
| `EL MA 2 - Sub Assy 1` | 5 |
| `EL MA 1 - Sub Assy 1` | 5 |
| `PRE HLA 1 - BIRTH` | 4 |
| `CUT 1 - PWTU` | 4 |
| `CUT 1 - PWTU LINK` | 4 |
| `GLUEB 1 - Glue Dispenser BOT` | 4 |
| `SWAVE 1 - SELECTIVE WAVE SOLDERING 1` | 4 |
| `PWTUT 1  - LINK (SOLDER WIRE)` | 4 |
| `FVT (BOARD) 1 - FVT` | 4 |
| `MSOLDER 2 - MANUAL SODLER 2` | 4 |
| `PRE ASSY 1 - Sub Assy 1` | 3 |
| `OQA 1` | 3 |
| `OVEN 1` | 3 |
| `PICKUP CAP REMOVAL 1` | 3 |
| `POP FLUX APPLICATION 1` | 3 |
| `MA 1/2 - RTV GLUE` | 3 |
| `UNDERFILLT1 (MAN)` | 3 |
| `MSOLDER 2 - M.SOLDERING 2` | 3 |
| `FVT (BOARD) 2 - FVT` | 3 |
| `MA 1/2 - LINK` | 3 |
| `MA 1/2 - GLUE INSPECTION` | 3 |
| `TEST (FVT RF) 1` | 3 |
| `TEST (FVT) 1` | 3 |
| `LABEL OUT 1 - LABEL INSPECTION` | 3 |
| `CWAVE 1 - CONVENTIONAL WAVE SOLDERING 1` | 3 |
| `CURING REFLOWB 1` | 3 |
| `CURING REFLOWT 1` | 3 |
| `UNDERFILL INSPECTIONT 1` | 3 |
| `UNDERFILL INSPECTIONB 1` | 3 |
| `UNDERFILLB 1 (MAN)` | 3 |
| `UNDERFILLB 1 (MAC)` | 3 |
| `LABEL OUT 1 - LINK` | 3 |
| `LOAD 1` | 3 |
| `UNDERFILLT 1 (MAC)` | 3 |
| `LABEL 1` | 3 |
| `LASER CUT 1` | 3 |
| `LABEL OUT 1 - LABELLING 1` | 3 |
| `HS MA 1 - Sub Assy 1` | 3 |
| `REFLOWT 2` | 3 |
| `TEST (FWDL TEST) 1` | 3 |
| `OBA 1 - OBA VIP` | 3 |
| `MA 1/2 - ROOM TEMP CURING` | 3 |
| `PACKOUT  - IPQC INSPECTION` | 2 |
| `FVT 1 - I2C Checking` | 2 |
| `ASOLDER (HOTBAR) 1` | 2 |
| `MA (THERMAL GEL) 1` | 2 |
| `TEST (TURN ON) 1 - Turn-On Test` | 2 |
| `HLA 2 - HLA MECH ASSY 2` | 2 |
| `HLA INSP 1` | 2 |
| `HOBA 1 - HOQA` | 2 |
| `HFNI 1 - HFNI` | 2 |
| `CURE 1 - LOCTITE CURING` | 2 |
| `LINK 1` | 2 |
| `GLUE 1 - LOCTITE DISPENSING` | 2 |
| `HLA 2 - HLA 2 LINK` | 2 |
| `MHTS TEST 1 - MOTOR AND HALL SENSOR TEST` | 2 |
| `MA 1/2 - PMI` | 2 |
| `MI 1 - SMART TORQUE 1` | 2 |
| `MA 1/2 - SMART TORQUE 2` | 2 |
| `POST COAT INSPB 1 - POST COATING INSPECTION BTM` | 1 |
| `POST COAT INSPT 1 - POST COATING INSPECTION TOP` | 1 |
| `SUB ASSY 1` | 1 |
| `HLA INSP 1 - QC HLA MAI` | 1 |
| `GLUET (TIM) 1` | 1 |
| `GLUEB (TIM) 1` | 1 |
| `FVT 5` | 1 |
| `FVT 4` | 1 |
| `FVT (DOM) 1 - DOM DOWNLOADING` | 1 |
| `PROG (CLPD) 1 - CPLD Programming` | 1 |
| `FNI 2` | 1 |
| `TEST 2` | 1 |

## 3. Per-customer × per-line process flow

Each table = one production line. Rows show every distinct
`(process, alias)` pair observed on that line, ordered alphabetically.
Re-order the rows to set the **standard flow** (top → bottom = step 1 → step N).

### ADVA

#### `ADVA BE 3F`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 4` | `(no alias)` |
| 3 | `Assembly 6` | `(no alias)` |
| 4 | `Assembly 7` | `(no alias)` |
| 5 | `Assembly 8` | `(no alias)` |
| 6 | `Assembly 9` | `(no alias)` |
| 7 | `FVT 1` | `(no alias)` |
| 8 | `FVT 2` | `(no alias)` |
| 9 | `FVT 3` | `(no alias)` |
| 10 | `FVT 4` | `(no alias)` |
| 11 | `FVT 5` | `(no alias)` |
| 12 | `FVT 6` | `(no alias)` |
| 13 | `FVT 7` | `(no alias)` |
| 14 | `Link 1` | `(no alias)` |

#### `ADVA HLA 3F`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 3` | `(no alias)` |
| 3 | `Assembly 7` | `(no alias)` |
| 4 | `FNI 1` | `(no alias)` |
| 5 | `FVT 1` | `(no alias)` |
| 6 | `FVT 2` | `(no alias)` |
| 7 | `FVT 3` | `(no alias)` |
| 8 | `Link 1` | `(no alias)` |
| 9 | `OBA 1` | `(no alias)` |
| 10 | `OBA 2` | `(no alias)` |
| 11 | `OBA 3` | `(no alias)` |
| 12 | `QC 1` | `(no alias)` |
| 13 | `QC 2` | `(no alias)` |
| 14 | `QC 3` | `(no alias)` |


### AKAMAI

#### `AKAMAI FATP BK1-1 B17 B18`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA MECH ASSY 1` |
| 2 | `FNI 1` | `HFNI 1` |
| 3 | `FNI 2` | `HFNI 2` |
| 4 | `FVT 1` | `FVT, FIRMWARE,NIC` |
| 5 | `FVT 2` | `PROVISIONING` |
| 6 | `Hi-Pot 1` | `HIPOT` |
| 7 | `OBA 1` | `OBA` |
| 8 | `Packout 1` | `PACKOUT` |


### AMAT

#### `AMAT HLA LCM P1C-1`  —  20 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `SUB MA 1 - Sub Assembly 1` |
| 2 | `Assembly 2` | `SUB MA 2 - Sub Assembly 2` |
| 3 | `Assembly 3` | `HLA 1 - HLA Mech Assy 1` |
| 4 | `Assembly 4` | `HLA 2 -HLA Mech Assy 2` |
| 5 | `Assembly 5` | `FA 1 - HLA Mech Assy 3 (FA)` |
| 6 | `FNI 1` | `FNI 1 - FNI` |
| 7 | `FVT 1` | `FVT 1 - Final Test` |
| 8 | `Link 1` | `SUB MA 1 - HLA BIRTH` |
| 9 | `Link 2` | `SUB MA 1 - HLA 1 LINK` |
| 10 | `Link 3` | `SUB MA 2 - HLA 2 LINK` |
| 11 | `Link 4` | `HLA 1- HLA 3 LINK` |
| 12 | `Link 5` | `HLA 2 - HLA 4 LINK` |
| 13 | `Link 6` | `FA 1 - HLA 5 LINK` |
| 14 | `OBA 1` | `FQC 1 - OQA (FQC)` |
| 15 | `Packout 1` | `PACKOUT - Pack Verify` |
| 16 | `Packout 2` | `PACKOUT - Packout` |
| 17 | `QC 1` | `SUB MA 1 - HLA MAI 1` |
| 18 | `QC 2` | `SUB MA 2 - HLA MAI 2` |
| 19 | `QC 3` | `HLA 1 - HLA MAI 3` |
| 20 | `QC 4` | `HLA 2 - HLA MAI 4` |


### ARISTA_NETWORKS_GLACIER

#### `ASNW BE 1/2RU P8-2`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 3` |
| 2 | `FNI 1` | `HFNI 1` |
| 3 | `Hi-Pot 1` | `HIPOT 1` |
| 4 | `Link 1` | `V LINK 1` |
| 5 | `OBA 1` | `HOBA 1` |
| 6 | `Packout 1` | `PACKOUT 1` |
| 7 | `Packout 2` | `PALLETIZING 1` |
| 8 | `QC 1` | `OCV 1` |
| 9 | `Test 1` | `FST 1` |

#### `ASNW BE 1RU SPEED P8-3`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2.1` |
| 3 | `Assembly 3` | `MA 2.2` |
| 4 | `QC 1` | `PMI 1` |

#### `ASNW BE 2RU P8-2`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Burn-In 1` | `BURN IN 1` |
| 2 | `ESS 1` | `ESS 1` |

#### `ASNW BE CELL P8-1`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 2.1` |
| 2 | `QC 1` | `PMI 1` |

#### `ASNW BE NPI P8-3`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `QC 1` | `PMI 1` |

#### `ASNW BE P8-1`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 3` |
| 2 | `Burn-In 1` | `BURN IN 1` |
| 3 | `ESS 1` | `ESS 1` |
| 4 | `FNI 1` | `HFNI 1` |
| 5 | `FVT 1` | `FVT 1` |
| 6 | `Link 1` | `V LINK 1` |
| 7 | `OBA 1` | `HOBA 1` |
| 8 | `Packout 1` | `PACKOUT 1` |
| 9 | `Packout 2` | `PALLETIZING 1` |
| 10 | `QC 1` | `OCV 1` |

#### `ASNW BE P8-3`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `LOOPBACK 1` |
| 2 | `Burn-In 1` | `BURN IN 1` |
| 3 | `ESS 1` | `ESS 1` |
| 4 | `FVT 1` | `FVT 1` |

#### `ASNW BE SEA TMA P8-1`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AVI 1` | `AVI 1` |
| 2 | `Assembly 1` | `MA 1` |
| 3 | `Assembly 2` | `MA 2.1` |
| 4 | `Assembly 3` | `MA 2.2` |
| 5 | `Assembly 4` | `MA 2.3` |
| 6 | `Assembly 5` | `MA 2.4` |
| 7 | `Assembly 6` | `MA 2.5` |
| 8 | `Assembly 7` | `MA 2.6` |
| 9 | `QC 1` | `PMI 1` |
| 10 | `QC 2` | `PMI 2` |

#### `ASNW BE SPEED 1 P8-3`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2.1` |
| 3 | `Assembly 3` | `MA 2.2` |
| 4 | `QC 1` | `PMI 1` |

#### `ASNW BE SPEED P8-1`  —  5 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2.1` |
| 3 | `Assembly 3` | `MA 2.2` |
| 4 | `Assembly 5` | `Loopback 1` |
| 5 | `QC 1` | `PMI 1` |

#### `ASNW HLA P8-1`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA (TMA) 3` |
| 2 | `FNI 1` | `FNI (TMA) 1` |
| 3 | `Hi-Pot 1` | `HIPOT (TMA) 1` |
| 4 | `Link 1` | `V LINK (TMA) 1` |
| 5 | `OBA 1` | `OBA (TMA) 1` |
| 6 | `Packout 1` | `PACKOUT (TMA) 1` |
| 7 | `Packout 2` | `PALLETIZING (TMA) 1` |
| 8 | `QC 1` | `OCV (TMA) 1` |
| 9 | `Test 1` | `FST (TMA) 1` |

#### `ASNW SMT P8-4 B831`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `BSI 1` | `BSI 1` |
| 4 | `Dispense 1` | `GLUEB 1` |
| 5 | `Handplace TOP 1` | `HANDPLACET 1` |
| 6 | `Label 1` | `BIRTH 1` |
| 7 | `Placement BOT 1` | `SMTB 1` |
| 8 | `Placement TOP 1` | `SMTT 1` |
| 9 | `Reflow BOT 1` | `REFLOWB 1` |
| 10 | `Reflow TOP 1` | `REFLOWT 1` |
| 11 | `SCR BOT 1` | `SCRB 1` |
| 12 | `SCR TOP 1` | `SCRT 1` |
| 13 | `SPI BOT 1` | `SPIB 1` |
| 14 | `SPI TOP 1` | `SPIT 1` |
| 15 | `TSI 1` | `TSI 1` |

#### `ASNW SMT P8-4 B832`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `BSI 1` | `BSI 1` |
| 4 | `Dispense 1` | `GLUEB 1` |
| 5 | `Label 1` | `BIRTH 1` |
| 6 | `Placement BOT 1` | `SMTB 1` |
| 7 | `Placement TOP 1` | `SMTT 1` |
| 8 | `Reflow BOT 1` | `REFLOWB 1` |
| 9 | `Reflow TOP 1` | `REFLOWT 1` |
| 10 | `SCR BOT 1` | `SCRB 1` |
| 11 | `SCR TOP 1` | `SCRT 1` |
| 12 | `SPI BOT 1` | `SPIB 1` |
| 13 | `SPI TOP 1` | `SPIT 1` |
| 14 | `TSI 1` | `TSI 1` |

#### `ASNW SMT P8-4 B833`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `Placement TOP 1` | `SMTT 1` |
| 4 | `Reflow BOT 1` | `REFLOWB 1` |
| 5 | `Reflow TOP 1` | `REFLOWT 1` |
| 6 | `SCR BOT 1` | `SCRB 1` |
| 7 | `SCR TOP 1` | `SCRT 1` |
| 8 | `SPI BOT 1` | `SPIB 1` |

#### `ASNW TH P8-4`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 2` | `SUBB (LIGHT PIPE) 1` |
| 2 | `Assembly 3` | `SUBT (LIGHT PIPE) 1` |
| 3 | `Assembly 4` | `PRE INSERTT 1` |
| 4 | `Assembly 5` | `PRE INSERTB 1` |
| 5 | `Depanel 1` | `ROUTER 1` |
| 6 | `ICT 1` | `FPROBE 1` |
| 7 | `ICT 2` | `ICT 1` |
| 8 | `Link 1` | `LINK (AOP) 1` |
| 9 | `MI 1` | `MI 1` |
| 10 | `Press 1` | `A PRESS FIT 1` |
| 11 | `Press 2` | `PRESS FITT 1` |
| 12 | `Press 3` | `PRESS FITB 1` |
| 13 | `Selective 1` | `S WAVE 1` |
| 14 | `Solder 1` | `M SOLDER 1` |
| 15 | `THI 1` | `TSTH 1` |
| 16 | `Touch Up 1` | `PWTU 1` |
| 17 | `XRAY 1` | `XRAY 1` |


### ASP

#### `ASP HLA ENDO P1B-2`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2` |
| 3 | `Burn-In 1` | `BURN IN` |
| 4 | `FNI 1` | `FNI` |
| 5 | `FVT 1` | `FVT` |
| 6 | `Hi-Pot 1` | `HI-PORT` |
| 7 | `OBA 1` | `OBA` |
| 8 | `Packout 1` | `PACKOUT` |
| 9 | `QC 1` | `MA INSP` |

#### `ASP HLA ENDO SUB P1B-2`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA (SUB)` |
| 2 | `Assembly 2` | `EBOX CRIMP` |
| 3 | `Assembly 3` | `EBOX MA` |
| 4 | `Assembly 4` | `WASH BASIN MA` |
| 5 | `FNI 1` | `FNI` |
| 6 | `OBA 1` | `OBA` |
| 7 | `Prep 1` | `EBOX PREP` |

#### `ASP HLA STOSA P1B-2`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2` |
| 3 | `Assembly 3` | `MA 3` |
| 4 | `Curing 1` | `CURING` |
| 5 | `FNI 1` | `FNI` |
| 6 | `FVT 1` | `FVT1 / FVT 4` |
| 7 | `FVT 2` | `FVT 2 / FVT 3` |
| 8 | `Hi-Pot 1` | `HI-PORT` |
| 9 | `OBA 1` | `OBA` |
| 10 | `Packout 1` | `PACKOUT` |
| 11 | `VMI 1` | `VMI` |


### BD

#### `BD BE PACK P1B-2 C12`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - LED LIGHT ON VERIFICATION` |
| 2 | `FNI 2` | `FNI 1 - FNI` |
| 3 | `FVT 1` | `FVT 1 - FVT 1` |
| 4 | `Link 1` | `FNI 1 - FNI LINK` |
| 5 | `OBA 1` | `OBA 1 - OQA` |
| 6 | `Packout 1` | `PACKOUT  - PACKOUT` |

#### `BD HLA P1B-2 C11`  —  5 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE HLA 1 - PRE ASSY 1` |
| 2 | `Label 1` | `PRE HLA 1 - BIRTH` |
| 3 | `Link 1` | `HLA INSP 1 - HLA 1 LINK` |
| 4 | `QC 1` | `HLA INSP 1 - QC HLA MAI` |
| 5 | `VMI 1` | `VMI 1 - VMI` |

#### `BD HLA PACK P1B-2 C10`  —  16 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1 - MA-1` |
| 2 | `Charging 1` | `CHARGE (BATT) 1 - BATTERY LEVEL CHECK` |
| 3 | `FNI 1` | `FNI 1 - FNI-1` |
| 4 | `FNI 2` | `QC 1 - HFNI OCR 1` |
| 5 | `FVT 2` | `FVT 1 - FVT1` |
| 6 | `FVT 3` | `FVT 1 - UL1` |
| 7 | `Label 1` | `MA 1 - BIRTH` |
| 8 | `Link 1` | `MA 1 - LINK` |
| 9 | `Link 5` | `PACKOUT  - PACKOUT LINK` |
| 10 | `OBA 1` | `OBA 1 - OQA1 TEST` |
| 11 | `OBA 2` | `OBA 1 - OQA1 INSPECTION` |
| 12 | `OBA 3` | `OBA 1 - OBA` |
| 13 | `Packout 1` | `PACK 1 - packing` |
| 14 | `Packout 2` | `PACKOUT  - PACKOUT` |
| 15 | `QC 1` | `QC 1 - HLA LABEL INSPECTION` |
| 16 | `QC 2` | `PACKOUT  - IPQC INSPECTION` |

#### `BD SMT P1A-1 B11a`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Label 1` | `BIRTH 1 - BIRTH` |
| 5 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 6 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 7 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 8 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 9 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 10 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 11 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 12 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 13 | `TSI 1` | `TSI 1 - TSI` |

#### `BD TH DEPANEL P1A-1 B9a`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER 1 - DEPANELING` |

#### `BD TH MI P1A-1 B11a`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `MIT 1 - MI TOP LINK` |
| 2 | `Link 2` | `PWTUT 1 - PWTU TOP LINK` |
| 3 | `Link 3` | `MIB 1 - MI BTM LINK` |
| 4 | `Link 4` | `PWTUB 1 - PWTU BTM LINK` |
| 5 | `MI 1` | `MIT 1 - MI_Top` |
| 6 | `MI 2` | `MIB 1 - MI BTM 1` |
| 7 | `Touch Up 1` | `PWTUT 1 - PWTU TOP` |
| 8 | `Touch Up 2` | `PWTUB 1 - PWTU BTM` |
| 9 | `Wave 1` | `CWAVET 1 - CONVENTIONAL WAVE SOLDERING TOP` |
| 10 | `Wave 2` | `CWAVEB 1 - CONVENTIONAL WAVE SOLDERING BTM` |

#### `BD TH WASH P1A-1 B11b`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1 - SMART TORQUE 1` |
| 2 | `Assembly 2` | `BACK MA 1 - BACK MECH ASSY 1` |
| 3 | `ICT 1` | `ICT 1 - ICT` |
| 4 | `Link 1` | `WASH 1 - WASH 1 LINK` |
| 5 | `Link 2` | `WASH 2 - WASH 2 LINK` |
| 6 | `Link 3` | `WASH 3 - WASH 3 LINK` |
| 7 | `Link 4` | `CWASH 4 - WASH 4 LINK` |
| 8 | `Link 5` | `ICT 1 - ICT LINK` |
| 9 | `Solder 1` | `MSOLDER 1 - M.SOLDERING 1` |
| 10 | `Solder 2` | `MSOLDER 2 - M.SOLDERING 2` |
| 11 | `THI 1` | `TSTHT 1 - TSTH TOP` |
| 12 | `THI 2` | `TSTHB 1 - TSTH BTM` |
| 13 | `THI 3` | `TSTH 1 - TSTH` |
| 14 | `Wash 1` | `WASH 1 - WASH 1` |
| 15 | `Wash 2` | `WASH 2 - WASH 2` |
| 16 | `Wash 3` | `WASH 3 - WASH 3` |
| 17 | `Wash 4` | `CWASH 4 - WASH 4` |

#### `BD TH XRAY P1A-1 B7b`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `XRAY 1` | `XRAY 1 - XRAY` |


### BECKMAN COULTER

#### `BEC BE CC P1A-1`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `CC QC 1` | `POST COAT INSPB 1 - POST COATING INSPECTION BTM` |
| 2 | `CC QC 2` | `POST COAT INSPT 1 - POST COATING INSPECTION TOP` |
| 3 | `CC Spray 1` | `ACOATB 1 - AUTO COATING BTM` |
| 4 | `CC Spray 2` | `ACOATT 1 - AUTO COATING TOP` |

#### `BEC BE MA P1A-1 B14b`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1 - BACK MECH ASSY 1` |
| 2 | `Assembly 2` | `MA 1 - BACK MECH ASSY 2` |
| 3 | `FNI 1` | `FNI 1 - FNI` |
| 4 | `FNI 2` | `FNI 1 - FNI VIP` |
| 5 | `Link 1` | `MA 1 - LINK 1` |
| 6 | `Link 2` | `PACKOUT - PACKOUT LINK` |
| 7 | `OBA 1` | `OBA 1 - OQA` |
| 8 | `OBA 2` | `OBA 1 - OQA VIP` |
| 9 | `Packout 1` | `PACKOUT - PACKOUT` |
| 10 | `QC 1` | `FNI 1 - VMI` |
| 11 | `QC 2` | `FNI 1 - VMIO` |

#### `BEC BE TEST P1B-2 B1a`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FVT 1` | `FVT 1 - FVT` |
| 2 | `FVT 2` | `FVT 2 - FVT1` |
| 3 | `Test 1` | `TEST (VERIF) 1 - TEST VERIFICATION` |

#### `BEC HLA P1B-2 B2a`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - FNI` |
| 2 | `FNI 2` | `FNI 1 - FNI VIP` |
| 3 | `Link 2` | `PACKOUT - PACKOUT LINK` |
| 4 | `OBA 1` | `OBA 1 - OBA` |
| 5 | `OBA 2` | `OBA 1 - OBA VIP` |
| 6 | `Packout 1` | `PACKOUT - PACKOUT` |

#### `BEC SMT P1A-1 B14a`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Dispense BOT 1` | `GLUEB 1 - Glue GLUEB01` |
| 5 | `Dispense TOP 1` | `GLUET 1 - Glue GLUET01` |
| 6 | `Label 1` | `BIRTH 1 - BIRTH` |
| 7 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 8 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 9 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 10 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 11 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 12 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 13 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 14 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 15 | `TSI 1` | `TSI 1 - TSI` |

#### `BEC TH AI P1A-1`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Auto Insert 1` | `AI 1 - AUTO INSERT 1` |
| 2 | `QC 1` | `AI INSP  1 - AI INSPECTION` |

#### `BEC TH P1A-1 B13b`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ICT 1` | `FPROBE 1 - FLYING PROBE` |
| 2 | `ICT 2` | `ICT 1 - ICT` |
| 3 | `Link 1` | `ASOLDER 1 - LINK` |
| 4 | `Link 2` | `PWTU 1 - PWTU LINK` |
| 5 | `MI 1` | `MI 1 - MI_1` |
| 6 | `Solder 1` | `ASOLDER 1 - ROBOTIC SOLDERING 1` |
| 7 | `THI 1` | `TSTH 1 - TSTH` |
| 8 | `Touch Up 1` | `PWTU 1 - PWTU` |
| 9 | `Wave 1` | `CWAVE 1 - WAVE CONVENTIONAL` |
| 10 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `BEC TH P1A-1 B14b`  —  16 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `FRONT MA 1 - FRONT MECH ASSY 1` |
| 2 | `Depanel 1` | `ROUTER 1 - DEPANELING` |
| 3 | `Link 1` | `WASH 1 - WASH LINK` |
| 4 | `Link 2` | `WASH 2 - WASH 1 LINK` |
| 5 | `Link 3` | `MSOLDER 1 - M.SOLDER 1 LINK` |
| 6 | `Link 4` | `UWASH 1 - WASH 2 LINK` |
| 7 | `Link 5` | `MSOLDER 1 - MANUAL SOLDERING 2 LINK` |
| 8 | `Press 1` | `PFIT 1 - PRESSFIT` |
| 9 | `QC 1` | `POST WASH 1 - POST WASH 1 INSP` |
| 10 | `QC 2` | `POST WASH 2 - POST WASH 2 INSP` |
| 11 | `QC 3` | `POST UWASH 1 - POST WASH 3 INSP` |
| 12 | `Solder 1` | `MSOLDER 1 - M.SOLDERING 2` |
| 13 | `Solder 2` | `MSOLDER 1 - M.SOLDERING 1` |
| 14 | `Wash 1` | `WASH 1 - WASH` |
| 15 | `Wash 2` | `WASH 2 - WASH 1` |
| 16 | `Wash 3` | `UWASH 1 - ULTROSONIC WASH 1` |


### DYSON

#### `DYSON BAY31_2F`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `(no alias)` |

#### `DYSON BAY32_2F`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 2` | `(no alias)` |
| 2 | `MI 1` | `(no alias)` |
| 3 | `OBA 1` | `(no alias)` |
| 4 | `Packout 1` | `(no alias)` |
| 5 | `Selective 1` | `(no alias)` |
| 6 | `Touch Up 1` | `(no alias)` |

#### `DYSON SMT BAY32 2F`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI TOP 1` | `(no alias)` |
| 2 | `Label 1` | `(no alias)` |
| 3 | `Label 2` | `(no alias)` |
| 4 | `Placement TOP 1` | `(no alias)` |
| 5 | `Reflow TOP 1` | `(no alias)` |
| 6 | `SCR TOP 1` | `(no alias)` |
| 7 | `SPI TOP 1` | `(no alias)` |

#### `DYSON X248 BPA`  —  32 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 18` | `(no alias)` |
| 11 | `Assembly 19` | `(no alias)` |
| 12 | `Assembly 2` | `(no alias)` |
| 13 | `Assembly 20` | `(no alias)` |
| 14 | `Assembly 21` | `(no alias)` |
| 15 | `Assembly 22` | `(no alias)` |
| 16 | `Assembly 3` | `(no alias)` |
| 17 | `Assembly 4` | `(no alias)` |
| 18 | `Assembly 5` | `(no alias)` |
| 19 | `Assembly 6` | `(no alias)` |
| 20 | `Assembly 7` | `(no alias)` |
| 21 | `Assembly 8` | `(no alias)` |
| 22 | `Assembly 9` | `(no alias)` |
| 23 | `FNI 1` | `(no alias)` |
| 24 | `Link 1` | `(no alias)` |
| 25 | `Link 2` | `(no alias)` |
| 26 | `Link 3` | `(no alias)` |
| 27 | `Packout 1` | `(no alias)` |
| 28 | `Test 1` | `(no alias)` |
| 29 | `Test 2` | `(no alias)` |
| 30 | `Test 3` | `(no alias)` |
| 31 | `Test 4` | `(no alias)` |
| 32 | `Test 5` | `(no alias)` |

#### `DYSON X248 CONEPACK`  —  38 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 18` | `(no alias)` |
| 11 | `Assembly 19` | `(no alias)` |
| 12 | `Assembly 2` | `(no alias)` |
| 13 | `Assembly 20` | `(no alias)` |
| 14 | `Assembly 21` | `(no alias)` |
| 15 | `Assembly 22` | `(no alias)` |
| 16 | `Assembly 23` | `(no alias)` |
| 17 | `Assembly 24` | `(no alias)` |
| 18 | `Assembly 26` | `(no alias)` |
| 19 | `Assembly 27` | `(no alias)` |
| 20 | `Assembly 3` | `(no alias)` |
| 21 | `Assembly 31` | `(no alias)` |
| 22 | `Assembly 32` | `(no alias)` |
| 23 | `Assembly 33` | `(no alias)` |
| 24 | `Assembly 34` | `(no alias)` |
| 25 | `Assembly 35` | `(no alias)` |
| 26 | `Assembly 36` | `(no alias)` |
| 27 | `Assembly 37` | `(no alias)` |
| 28 | `Assembly 38` | `(no alias)` |
| 29 | `Assembly 39` | `(no alias)` |
| 30 | `Assembly 4` | `(no alias)` |
| 31 | `Assembly 5` | `(no alias)` |
| 32 | `Assembly 6` | `(no alias)` |
| 33 | `Assembly 7` | `(no alias)` |
| 34 | `Assembly 8` | `(no alias)` |
| 35 | `Assembly 9` | `(no alias)` |
| 36 | `Link 1` | `(no alias)` |
| 37 | `Packout 1` | `(no alias)` |
| 38 | `Test 1` | `(no alias)` |

#### `DYSON X248 MAINBODY`  —  46 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 18` | `(no alias)` |
| 11 | `Assembly 19` | `(no alias)` |
| 12 | `Assembly 2` | `(no alias)` |
| 13 | `Assembly 20` | `(no alias)` |
| 14 | `Assembly 21` | `(no alias)` |
| 15 | `Assembly 22` | `(no alias)` |
| 16 | `Assembly 23` | `(no alias)` |
| 17 | `Assembly 24` | `(no alias)` |
| 18 | `Assembly 25` | `(no alias)` |
| 19 | `Assembly 26` | `(no alias)` |
| 20 | `Assembly 27` | `(no alias)` |
| 21 | `Assembly 28` | `(no alias)` |
| 22 | `Assembly 29` | `(no alias)` |
| 23 | `Assembly 3` | `(no alias)` |
| 24 | `Assembly 30` | `(no alias)` |
| 25 | `Assembly 31` | `(no alias)` |
| 26 | `Assembly 32` | `(no alias)` |
| 27 | `Assembly 33` | `(no alias)` |
| 28 | `Assembly 34` | `(no alias)` |
| 29 | `Assembly 35` | `(no alias)` |
| 30 | `Assembly 36` | `(no alias)` |
| 31 | `Assembly 37` | `(no alias)` |
| 32 | `Assembly 38` | `(no alias)` |
| 33 | `Assembly 39` | `(no alias)` |
| 34 | `Assembly 4` | `(no alias)` |
| 35 | `Assembly 40` | `(no alias)` |
| 36 | `Assembly 5` | `(no alias)` |
| 37 | `Assembly 6` | `(no alias)` |
| 38 | `Assembly 7` | `(no alias)` |
| 39 | `Assembly 8` | `(no alias)` |
| 40 | `Assembly 9` | `(no alias)` |
| 41 | `Link 1` | `(no alias)` |
| 42 | `Link 2` | `(no alias)` |
| 43 | `Packout 1` | `(no alias)` |
| 44 | `Test 1` | `(no alias)` |
| 45 | `Test 2` | `(no alias)` |
| 46 | `Test 3` | `(no alias)` |

#### `DYSON X248 MAINLINE`  —  63 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 18` | `(no alias)` |
| 11 | `Assembly 19` | `(no alias)` |
| 12 | `Assembly 2` | `(no alias)` |
| 13 | `Assembly 20` | `(no alias)` |
| 14 | `Assembly 21` | `(no alias)` |
| 15 | `Assembly 22` | `(no alias)` |
| 16 | `Assembly 23` | `(no alias)` |
| 17 | `Assembly 24` | `(no alias)` |
| 18 | `Assembly 25` | `(no alias)` |
| 19 | `Assembly 26` | `(no alias)` |
| 20 | `Assembly 27` | `(no alias)` |
| 21 | `Assembly 28` | `(no alias)` |
| 22 | `Assembly 29` | `(no alias)` |
| 23 | `Assembly 3` | `(no alias)` |
| 24 | `Assembly 30` | `(no alias)` |
| 25 | `Assembly 31` | `(no alias)` |
| 26 | `Assembly 32` | `(no alias)` |
| 27 | `Assembly 33` | `(no alias)` |
| 28 | `Assembly 34` | `(no alias)` |
| 29 | `Assembly 35` | `(no alias)` |
| 30 | `Assembly 36` | `(no alias)` |
| 31 | `Assembly 4` | `(no alias)` |
| 32 | `Assembly 5` | `(no alias)` |
| 33 | `Assembly 6` | `(no alias)` |
| 34 | `Assembly 7` | `(no alias)` |
| 35 | `Assembly 8` | `(no alias)` |
| 36 | `Assembly 9` | `(no alias)` |
| 37 | `FNI 1` | `(no alias)` |
| 38 | `FNI 2` | `(no alias)` |
| 39 | `Link 1` | `(no alias)` |
| 40 | `Link 2` | `(no alias)` |
| 41 | `Link 3` | `(no alias)` |
| 42 | `Link 4` | `(no alias)` |
| 43 | `Link 5` | `(no alias)` |
| 44 | `OBA 1` | `(no alias)` |
| 45 | `OBA 2` | `(no alias)` |
| 46 | `Packout 1` | `(no alias)` |
| 47 | `Test 1` | `(no alias)` |
| 48 | `Test 10` | `(no alias)` |
| 49 | `Test 11` | `(no alias)` |
| 50 | `Test 12` | `(no alias)` |
| 51 | `Test 13` | `(no alias)` |
| 52 | `Test 14` | `(no alias)` |
| 53 | `Test 15` | `(no alias)` |
| 54 | `Test 16` | `(no alias)` |
| 55 | `Test 17` | `(no alias)` |
| 56 | `Test 2` | `(no alias)` |
| 57 | `Test 3` | `(no alias)` |
| 58 | `Test 4` | `(no alias)` |
| 59 | `Test 5` | `(no alias)` |
| 60 | `Test 6` | `(no alias)` |
| 61 | `Test 7` | `(no alias)` |
| 62 | `Test 8` | `(no alias)` |
| 63 | `Test 9` | `(no alias)` |

#### `DYSON X277 BPA B_25`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 2` | `(no alias)` |
| 3 | `Assembly 3` | `(no alias)` |
| 4 | `FNI 1` | `(no alias)` |
| 5 | `Link 1` | `(no alias)` |
| 6 | `Packout 1` | `(no alias)` |
| 7 | `Test 1` | `(no alias)` |
| 8 | `Test 2` | `(no alias)` |
| 9 | `Test 3` | `(no alias)` |

#### `DYSON X277 BPA SLAVE`  —  20 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 2` | `(no alias)` |
| 10 | `Assembly 3` | `(no alias)` |
| 11 | `Assembly 4` | `(no alias)` |
| 12 | `Assembly 5` | `(no alias)` |
| 13 | `Assembly 6` | `(no alias)` |
| 14 | `Assembly 7` | `(no alias)` |
| 15 | `Assembly 8` | `(no alias)` |
| 16 | `Assembly 9` | `(no alias)` |
| 17 | `Link 1` | `(no alias)` |
| 18 | `Test 1` | `(no alias)` |
| 19 | `Test 2` | `(no alias)` |
| 20 | `Test 3` | `(no alias)` |

#### `DYSON X277 CYCLONE`  —  22 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 2` | `(no alias)` |
| 11 | `Assembly 3` | `(no alias)` |
| 12 | `Assembly 4` | `(no alias)` |
| 13 | `Assembly 5` | `(no alias)` |
| 14 | `Assembly 6` | `(no alias)` |
| 15 | `Assembly 7` | `(no alias)` |
| 16 | `Assembly 8` | `(no alias)` |
| 17 | `Assembly 9` | `(no alias)` |
| 18 | `FNI 1` | `(no alias)` |
| 19 | `Link 1` | `(no alias)` |
| 20 | `Packout 1` | `(no alias)` |
| 21 | `Test 1` | `(no alias)` |
| 22 | `Test 2` | `(no alias)` |

#### `DYSON X277 DOCK`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 2` | `(no alias)` |
| 3 | `Assembly 3` | `(no alias)` |
| 4 | `Assembly 4` | `(no alias)` |
| 5 | `Assembly 5` | `(no alias)` |
| 6 | `Assembly 6` | `(no alias)` |
| 7 | `Assembly 7` | `(no alias)` |
| 8 | `FNI 1` | `(no alias)` |
| 9 | `Link 1` | `(no alias)` |
| 10 | `Link 2` | `(no alias)` |
| 11 | `Packout 1` | `(no alias)` |

#### `DYSON X277 LOWERBODY`  —  49 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 11` | `(no alias)` |
| 4 | `Assembly 12` | `(no alias)` |
| 5 | `Assembly 13` | `(no alias)` |
| 6 | `Assembly 14` | `(no alias)` |
| 7 | `Assembly 15` | `(no alias)` |
| 8 | `Assembly 16` | `(no alias)` |
| 9 | `Assembly 17` | `(no alias)` |
| 10 | `Assembly 18` | `(no alias)` |
| 11 | `Assembly 19` | `(no alias)` |
| 12 | `Assembly 2` | `(no alias)` |
| 13 | `Assembly 20` | `(no alias)` |
| 14 | `Assembly 21` | `(no alias)` |
| 15 | `Assembly 22` | `(no alias)` |
| 16 | `Assembly 23` | `(no alias)` |
| 17 | `Assembly 24` | `(no alias)` |
| 18 | `Assembly 25` | `(no alias)` |
| 19 | `Assembly 26` | `(no alias)` |
| 20 | `Assembly 27` | `(no alias)` |
| 21 | `Assembly 28` | `(no alias)` |
| 22 | `Assembly 29` | `(no alias)` |
| 23 | `Assembly 3` | `(no alias)` |
| 24 | `Assembly 30` | `(no alias)` |
| 25 | `Assembly 31` | `(no alias)` |
| 26 | `Assembly 32` | `(no alias)` |
| 27 | `Assembly 33` | `(no alias)` |
| 28 | `Assembly 34` | `(no alias)` |
| 29 | `Assembly 4` | `(no alias)` |
| 30 | `Assembly 5` | `(no alias)` |
| 31 | `Assembly 6` | `(no alias)` |
| 32 | `Assembly 7` | `(no alias)` |
| 33 | `Assembly 8` | `(no alias)` |
| 34 | `Assembly 9` | `(no alias)` |
| 35 | `FNI 1` | `(no alias)` |
| 36 | `Link 1` | `(no alias)` |
| 37 | `Link 10` | `(no alias)` |
| 38 | `Link 2` | `(no alias)` |
| 39 | `Link 3` | `(no alias)` |
| 40 | `Link 4` | `(no alias)` |
| 41 | `Link 5` | `(no alias)` |
| 42 | `Link 6` | `(no alias)` |
| 43 | `Link 7` | `(no alias)` |
| 44 | `Link 8` | `(no alias)` |
| 45 | `Link 9` | `(no alias)` |
| 46 | `Packout 1` | `(no alias)` |
| 47 | `Test 1` | `(no alias)` |
| 48 | `Test 2` | `(no alias)` |
| 49 | `Test 3` | `(no alias)` |


### ELENION TECHNOLOGIES

#### `ELENION BE 3F`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Curing 1` | `CLEAN (PLASMA) 1` |
| 2 | `Curing 2` | `CURE 1` |
| 3 | `Link 1` | `BE BIRTH 1` |
| 4 | `Link 2` | `LINK (OPTIC) 1` |
| 5 | `Link 3` | `VER (FIBER) 1` |
| 6 | `Oven 1` | `BAKE (EEN) 1` |
| 7 | `Oven 2` | `BAKE 1` |
| 8 | `QC 1` | `VMI 1` |
| 9 | `Wash 1` | `OFF CLEAN (EEN) 1` |

#### `ELENION HLA 3F`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE MA 1` |
| 2 | `Assembly 2` | `BMA 2` |
| 3 | `Assembly 3` | `SUB MA 1` |
| 4 | `Assembly 4` | `SUB MA 2` |
| 5 | `FVT 1` | `FVT (DCEO) 1` |
| 6 | `FVT 2` | `FVT (BER) 1` |
| 7 | `Label 1` | `LABEL (LASER) 1` |
| 8 | `Link 1` | `HLA BIRTH 1` |
| 9 | `Oven 1` | `BAKE 2` |
| 10 | `Oven 2` | `BAKE 3` |
| 11 | `Oven 3` | `BAKE 1` |
| 12 | `QC 1` | `PRE MA 2` |
| 13 | `QC 2` | `MAI 2` |
| 14 | `QC 3` | `MAI 3` |
| 15 | `QC 4` | `INSP (OPTIC) 1` |
| 16 | `QC 5` | `INSP (OPTIC) 3` |
| 17 | `QC 6` | `INSP (OPTIC) 4` |

#### `ELENION SUB 3F`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `BE BIRTH 1` |
| 2 | `Oven 1` | `BAKE 1` |
| 3 | `Oven 2` | `PRE COND 1` |
| 4 | `Packout 1` | `VER (FIBER) 1` |


### ENDURANCE

#### `ENDURANCE SMT BK1-2 B202`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `BSI 1` | `BSI 1` |
| 4 | `Label 1` | `BIRTH ` |
| 5 | `Placement BOT 1` | `SMTB 1` |
| 6 | `Placement TOP 1` | `SMTT1` |
| 7 | `Reflow BOT 1` | `REFLOWB 1` |
| 8 | `Reflow TOP 1` | `REFLOWT 1` |
| 9 | `SCR BOT 1` | `SCRB 1` |
| 10 | `SCR TOP 1` | `SCRT 1` |
| 11 | `TSI 1` | `TSI 1` |

#### `ENDURANCE TH BK1-1 B18`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AVI 1` | `MAGIC RAY` |
| 2 | `Assembly 1` | `BACK MECH ASSY 1` |
| 3 | `Assembly 2` | `BACK MECH ASSY 2` |
| 4 | `FNI 1` | `FNI 1` |
| 5 | `FVT 1` | `BST` |
| 6 | `FVT 2` | `FVT` |
| 7 | `OBA 1` | `OBA` |
| 8 | `Packout 1` | `PACKOUT` |

#### `ENDURANCE TH BK1-2 B202`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER` |
| 2 | `FNI 1` | `AOP FNI` |
| 3 | `ICT 1` | `ICT` |
| 4 | `MI 1` | `MI TOP` |
| 5 | `Touch Up 1` | `PWTU` |
| 6 | `Wave 1` | `WAVE` |
| 7 | `XRAY 1` | `XRAY` |


### FORTALEZA

#### `FORTA HDMT SI BK1-2`  —  19 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `FRONT MA 1` |
| 2 | `Assembly 10` | `MA 10` |
| 3 | `Assembly 2` | `FRONT MA 2` |
| 4 | `Assembly 3` | `FRONT MA 3` |
| 5 | `Assembly 4` | `MA 4` |
| 6 | `Assembly 5` | `MA 5` |
| 7 | `Assembly 6` | `HLA 1` |
| 8 | `Assembly 7` | `HLA 2` |
| 9 | `Assembly 8` | `MA 8` |
| 10 | `Assembly 9` | `MA 9` |
| 11 | `Birth 1` | `(no alias)` |
| 12 | `FNI 1` | `FNI 1` |
| 13 | `FNI 2` | `HFNI 1` |
| 14 | `FNI 3` | `FNI 3` |
| 15 | `FVT 1` | `FVT 1` |
| 16 | `FVT 2` | `FVT 2` |
| 17 | `Leak Test 1` | `TEST (COM LEAK) 1` |
| 18 | `OBA 1` | `OBA 1` |
| 19 | `Packout 1` | `PACKOUT 1` |

#### `FORTA SMT BK1-2 B202`  —  35 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `Assembly 1` | `MA 1` |
| 4 | `Assembly 3` | `MA 3` |
| 5 | `BSI 1` | `BSI 1` |
| 6 | `Depanel 1` | `ROUTER 1` |
| 7 | `Dispense TOP 1` | `(no alias)` |
| 8 | `FNI 1` | `FNI 1` |
| 9 | `FVT 1` | `FVT 1` |
| 10 | `Handplace BOT 1` | `HANDPLACEB 1` |
| 11 | `Handplace TOP 1` | `HANDPLACET 1` |
| 12 | `ICT 1` | `ICT 1` |
| 13 | `ICT 2` | `ICT 2` |
| 14 | `Label 1` | `BIRTH 1` |
| 15 | `MI 1` | `MIT 1` |
| 16 | `MI 2` | `MIT 1` |
| 17 | `OBA 1` | `OBA 1` |
| 18 | `Packout 1` | `PACKOUT 1` |
| 19 | `Placement BOT 1` | `SMTB 1` |
| 20 | `Placement TOP 1` | `SMTT 1` |
| 21 | `Press 1` | `PRESS FIT 1` |
| 22 | `Press 2` | `PRESS FITB 1` |
| 23 | `Reflow BOT 1` | `REFLOWB 1` |
| 24 | `Reflow TOP 1` | `REFLOWT 1` |
| 25 | `SCR BOT 1` | `SCRB 1` |
| 26 | `SCR TOP 1` | `SCRT 1` |
| 27 | `SPI BOT 1` | `SPIB 1` |
| 28 | `SPI TOP 1` | `SPIT 1` |
| 29 | `Selective 1` | `S WAVET 1` |
| 30 | `Solder 1` | `M SOLDER 1` |
| 31 | `THI 1` | `TSTH 1` |
| 32 | `TSI 1` | `TSI 1` |
| 33 | `Touch Up 1` | `PWTU 1` |
| 34 | `Wave 1` | `C WAVET 1` |
| 35 | `XRAY 1` | `XRAY 1` |

#### `FORTA TH BK1-2 B202`  —  18 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `MA 2` |
| 3 | `Assembly 3` | `MA 3` |
| 4 | `Depanel 1` | `ROUTER 1` |
| 5 | `FNI 1` | `FNI 1` |
| 6 | `FVT 1` | `FVT 1` |
| 7 | `FVT 2` | `FVT 2` |
| 8 | `ICT 1` | `ICT 1` |
| 9 | `ICT 2` | `FPROBE 1` |
| 10 | `MI 1` | `MIT 1` |
| 11 | `OBA 1` | `OBA 1` |
| 12 | `Packout 1` | `PACKOUT` |
| 13 | `Press 1` | `PRESS FIT 1` |
| 14 | `Press 2` | `PRESS FIT 2` |
| 15 | `Program 1` | `PROG (EEPROM) 1` |
| 16 | `Solder 1` | `M SOLDER 1` |
| 17 | `Touch Up 1` | `PWTU 1` |
| 18 | `Wave 1` | `C WAVET 1` |


### GOPRO

#### `GOPRO SMT BK2-2 B36`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `Assembly 1` | `PICKUP CAP REMOVAL 1` |
| 4 | `Birth 1` | `BIRTH 1` |
| 5 | `Dispense 1` | `POP FLUX APPLICATION 1` |
| 6 | `Label 1` | `LABEL 1` |
| 7 | `Load 1` | `LOAD 1` |
| 8 | `Placement BOT 1` | `SMTB 1` |
| 9 | `Placement TOP 1` | `SMTT 1` |
| 10 | `Reflow BOT 1` | `REFLOWB 1` |
| 11 | `Reflow TOP 1` | `REFLOWT 1` |
| 12 | `Reflow TOP 2` | `REFLOWT 2` |
| 13 | `SCR BOT 1` | `SCRB 1` |
| 14 | `SCR TOP 1` | `SCRT 1` |
| 15 | `SPI BOT 1` | `SPIB 1` |
| 16 | `SPI TOP 1` | `SPIT 1` |
| 17 | `XRAY 1` | `XRAY 1` |

#### `GOPRO TH BK2-2 B36`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `LASER CUT 1` |
| 2 | `Dispense 1` | `UNDERFILLB 1 (MAN)` |
| 3 | `Dispense 2` | `UNDERFILLB 1 (MAC)` |
| 4 | `Dispense 3` | `UNDERFILLT1 (MAN)` |
| 5 | `Dispense 4` | `UNDERFILLT 1 (MAC)` |
| 6 | `FNI 1` | `FNI 1` |
| 7 | `OBA 1` | `OQA 1` |
| 8 | `Packout 1` | `PACKOUT 1` |
| 9 | `Reflow BOT 1` | `CURING REFLOWB 1` |
| 10 | `Reflow TOP 1` | `CURING REFLOWT 1` |
| 11 | `Test 1` | `TEST (FWDL TEST) 1` |
| 12 | `Test 2` | `TEST (FVT) 1` |
| 13 | `Test 3` | `TEST (FVT RF) 1` |
| 14 | `VMI 1` | `UNDERFILL INSPECTIONB 1` |
| 15 | `VMI 2` | `UNDERFILL INSPECTIONT 1` |


### HMB

#### `HMB HLA C38 FATP BK2-2 B31`  —  28 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Assembly 2` | `(no alias)` |
| 3 | `Assembly 3` | `(no alias)` |
| 4 | `Assembly 4` | `(no alias)` |
| 5 | `Assembly 5` | `(no alias)` |
| 6 | `Assembly 6` | `(no alias)` |
| 7 | `Birth 1` | `(no alias)` |
| 8 | `FNI 1` | `(no alias)` |
| 9 | `Link 1` | `(no alias)` |
| 10 | `Link 2` | `(no alias)` |
| 11 | `Link 3` | `(no alias)` |
| 12 | `Link 4` | `(no alias)` |
| 13 | `Link 5` | `(no alias)` |
| 14 | `Link 6` | `(no alias)` |
| 15 | `OBA 1` | `(no alias)` |
| 16 | `Packout 1` | `(no alias)` |
| 17 | `Test 1` | `(no alias)` |
| 18 | `Test 10` | `(no alias)` |
| 19 | `Test 2` | `(no alias)` |
| 20 | `Test 3` | `(no alias)` |
| 21 | `Test 4` | `(no alias)` |
| 22 | `Test 5` | `(no alias)` |
| 23 | `Test 6` | `(no alias)` |
| 24 | `Test 7` | `(no alias)` |
| 25 | `Test 8` | `(no alias)` |
| 26 | `Test 9` | `(no alias)` |
| 27 | `VMI 1` | `(no alias)` |
| 28 | `VMI 2` | `(no alias)` |

#### `HMB HLA C38 SUB BK2-2 B31`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE ASSY 1 - Sub Assy 1` |
| 2 | `Assembly 10` | `LID MA 1 - Sub Assy 1` |
| 3 | `Assembly 11` | `LID MA 2 - Sub Assy 1` |
| 4 | `Assembly 12` | `LID MA 3 - Sub Assy 1` |
| 5 | `Assembly 2` | `HS MA 1 - Sub Assy 1` |
| 6 | `Assembly 3` | `EL MA 1 - Sub Assy 1` |
| 7 | `Assembly 4` | `EL MA 2 - Sub Assy 1` |
| 8 | `Assembly 5` | `SBL MA 1 - Sub Assy 1` |
| 9 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 10 | `Curing 1` | `CURE 1 - CURING` |
| 11 | `Link 1` | `HLA 1 - HLA 1 LINK` |
| 12 | `Link 5` | `HLA 1 - HLA 1 LINK` |
| 13 | `Packout 1` | `PACKOUT TRANSFER - PACKOUTTRANSFER` |
| 14 | `VMI 1` | `VMI 1 - VMI` |

#### `HMB HLA G47 FATP BK2-2 B31`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1 - HLA MECH ASSY 1` |
| 2 | `Assembly 2` | `HLA 2 - HLA MECH ASSY 2` |
| 3 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 4 | `FNI 1` | `HFNI 1 - HFNI` |
| 5 | `Link 1` | `HLA 1 - HLA 1 LINK` |
| 6 | `Link 2` | `HLA 2 - HLA 2 LINK` |
| 7 | `OBA 1` | `HOBA 1 - HOQA` |
| 8 | `Packout 1` | `PACKOUT 1 - PACKOUT` |
| 9 | `Test 1` | `MHTS TEST 1 - MOTOR AND HALL SENSOR TEST` |


### ILLUMINA

#### `ILMN BE P1B-3`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - FNI` |
| 2 | `OBA 1` | `OBA 1 - OQA` |
| 3 | `Packout 1` | `PACKOUT  - PACKOUT` |

#### `ILMN CHS SUB P1B-3`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1 - HLA MECH ASSY` |
| 2 | `Assembly 2` | `HLA 1 - HLA MECH ASSY 1` |
| 3 | `Assembly 3` | `HLA 1 - HLA MECH ASSY 2` |
| 4 | `Birth 1` | `HLA 1 - HLA BIRTH` |
| 5 | `FNI 1` | `FNI 1 - HFNI` |
| 6 | `FVT 1` | `FVT 1 - FVT 1` |
| 7 | `FVT 2` | `FVT 1 - FVT 2` |
| 8 | `Hi-Pot 1` | `HIPOT 1 - HIPOT` |
| 9 | `Link 1` | `HLA 1 - HLA LINK` |
| 10 | `Link 2` | `HLA 1 - HLA 2 LINK` |
| 11 | `OBA 1` | `OBA 1 - HOBA` |
| 12 | `Packout 1` | `PACKOUT - PACKOUT` |
| 13 | `QC 1` | `HLA 1 - HLA MAI 2` |

#### `ILMN ENC SUB P1B-3`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1 - HLA MECH ASSY` |
| 2 | `Assembly 2` | `HLA 1 - HLA MECH ASSY 1` |
| 3 | `Assembly 3` | `HLA 1 - HLA MECH ASSY 2` |
| 4 | `Birth 1` | `HLA 1 - HLA BIRTH` |
| 5 | `FNI 1` | `FNI 1 - HFNI` |
| 6 | `FVT 1` | `FVT 1 - FVT 1` |
| 7 | `Link 1` | `HLA 1 - HLA LINK` |
| 8 | `Link 2` | `HLA 1 - HLA 1 LINK` |
| 9 | `Link 3` | `HLA 1 - HLA 2 LINK` |
| 10 | `OBA 1` | `OBA 1 - HOBA` |
| 11 | `Packout 1` | `PACKOUT - PACKOUT` |
| 12 | `QC 1` | `HLA 1 - HLA MAI 1` |
| 13 | `QC 2` | `HLA 1 - HLA MAI 2` |

#### `ILMN FCC HLA P1B-3`  —  12 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1 - HLA MECH ASSY 1` |
| 2 | `Assembly 2` | `HLA 1 - HLA MECH ASSY 2` |
| 3 | `Birth 1` | `HLA 1 - HLA BIRTH` |
| 4 | `FNI 1` | `FNI 1 - HFNI` |
| 5 | `FVT 1` | `FVT 1 - FVT 1` |
| 6 | `FVT 2` | `FVT 1 - FVT 2` |
| 7 | `Link 1` | `HLA 1 - HLA LINK` |
| 8 | `Link 2` | `HLA 1 - HLA 2 LINK` |
| 9 | `OBA 1` | `OBA 1 - HOBA` |
| 10 | `Packout 1` | `PACKOUT - PACKOUT` |
| 11 | `QC 1` | `HLA 1 - HLA MAI 1` |
| 12 | `QC 2` | `HLA 1 - HLA MAI 2` |

#### `ILMN HLA CHS P1B-3`  —  29 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1 - HLA MECH ASSY` |
| 2 | `Assembly 2` | `HLA 1 - HLA MECH ASSY 2` |
| 3 | `Assembly 3` | `HLA 1 - HLA MECH ASSY 3` |
| 4 | `Assembly 4` | `HLA 1 - HLA MECH ASSY 4` |
| 5 | `Assembly 5` | `HLA 5 - HLA MECH ASSY 5` |
| 6 | `Birth 1` | `HLA 1 - HLA BIRTH` |
| 7 | `FNI 1` | `FNI 1 - HFNI` |
| 8 | `FVT 1` | `FVT 1 - FVT 1` |
| 9 | `FVT 10` | `FVT 1 - FVT 10` |
| 10 | `FVT 2` | `FVT 1 - FVT 2` |
| 11 | `FVT 3` | `FVT 1 - FVT 3` |
| 12 | `FVT 4` | `FVT 1 - FVT 4` |
| 13 | `FVT 5` | `FVT 1 - FVT 5` |
| 14 | `FVT 6` | `FVT 1 - FVT 6` |
| 15 | `FVT 7` | `FVT 1 - FVT 7` |
| 16 | `FVT 8` | `FVT 1 - FVT 8` |
| 17 | `FVT 9` | `FVT 1 - FVT 9` |
| 18 | `Hi-Pot 1` | `HIPOT 1 - HIPOT` |
| 19 | `Link 1` | `HLA 1 - HLA 1 LINK` |
| 20 | `Link 2` | `HLA 1 - HLA 2 LINK` |
| 21 | `Link 3` | `HLA 1 - HLA 3 LINK` |
| 22 | `Link 4` | `HLA 1 - HLA 4 LINK` |
| 23 | `Link 5` | `HLA 5 - HLA 5 LINK` |
| 24 | `OBA 1` | `OBA 1 - HOBA` |
| 25 | `Packout 1` | `PACKOUT - PACKOUT` |
| 26 | `QC 1` | `HLA 1 - HLA MAI 1` |
| 27 | `QC 2` | `HLA 1 - HLA MAI 2` |
| 28 | `QC 3` | `HLA 1 - HLA MAI 3` |
| 29 | `QC 4` | `HLA 1 - HLA MAI 4` |

#### `ILMN SMT P1A B5a`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 2 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 3 | `Label 1` | `BIRTH 1 - LABELING` |
| 4 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 5 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 6 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 7 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 8 | `TSI 1` | `TSI 1 - TSI` |

#### `ILMN TH DEPANEL P1A B5a`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER 1 - DEPANELING` |

#### `ILMN TH P1A B12b`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `LINK AOP - AOP FNI` |
| 2 | `MI 1` | `MIB 1 - MI BTM 1` |
| 3 | `Solder 1` | `MSOLDER 1 - M.SOLDERING` |
| 4 | `THI 1` | `TSTH 1 - TSTH` |
| 5 | `Touch Up 1` | `PWTU 1 - PWTU` |
| 6 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `ILMN TH WASH P1A B6b`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Wash 1` | `WASH 1 - WASH 1` |
| 2 | `Wash 2` | `WASH 2 - WASH 2` |


### INTEL OPTICS

#### `INTEL BK_3F_CHAMBER`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Test 1` | `(no alias)` |

#### `PHOTONICS BK_3F_B32B`  —  21 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1` |
| 2 | `Assembly 2` | `BACK MA 2` |
| 3 | `Assembly 3` | `BACK MA 3` |
| 4 | `Assembly 4` | `BACK MA 4` |
| 5 | `Assembly 5` | `BACK MA 5` |
| 6 | `Assembly 6` | `BACK MA 6` |
| 7 | `Assembly 8` | `BACK MA 8` |
| 8 | `FNI 1` | `FNI 1` |
| 9 | `FNI 2` | `FNI 2` |
| 10 | `OBA 1` | `OBA 1` |
| 11 | `OBA 2` | `OBA 2` |
| 12 | `Packout 1` | `PACKOUT 1` |
| 13 | `Test 1` | `TEST 1` |
| 14 | `Test 2` | `TEST 2` |
| 15 | `Test 3` | `TEST 3` |
| 16 | `Test 4` | `TEST 4` |
| 17 | `Test 5` | `TEST 5` |
| 18 | `Test 6` | `TEST 6` |
| 19 | `Test 7` | `TEST 7` |
| 20 | `Test 8` | `TEST 8` |
| 21 | `Test 9` | `TEST 9` |

#### `PHOTONICS BK_3F_B32C`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1` |
| 2 | `Assembly 2` | `BACK MA 2` |
| 3 | `Assembly 3` | `BACK MA 3` |
| 4 | `Assembly 5` | `BACK MA 5` |
| 5 | `Test 1` | `TEST 1` |
| 6 | `Test 3` | `TEST 3` |
| 7 | `Test 4` | `TEST 4` |
| 8 | `Test 5` | `TEST 5` |
| 9 | `Test 6` | `TEST 6` |
| 10 | `Test 7` | `TEST 7` |
| 11 | `Test 8` | `TEST 8` |

#### `PHOTONICS BK_3F_B35A`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Placement BOT 1` | `SMTB 1` |
| 2 | `Placement TOP 1` | `SMTT 1` |
| 3 | `Placement TOP 2` | `SMTT 2` |
| 4 | `Test 1` | `TEST 1 ` |
| 5 | `VMI 1` | `VMI 1` |
| 6 | `VMI 2` | `VMI 2` |
| 7 | `VMI 3` | `VMI 3` |

#### `PHOTONICS BK_3F_B35B`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI 1` | `AOIBE 1` |
| 2 | `Oven 1` | `BAKE 1` |
| 3 | `Oven 2` | `BAKE 2` |
| 4 | `Oven 3` | `BAKE 3` |

#### `PHOTONICS BK_3F_B36`  —  21 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI 1` | `AOIBE 1` |
| 2 | `Assembly 1` | `BACK MA 1` |
| 3 | `Assembly 2` | `BACK MA 2` |
| 4 | `Assembly 3` | `BACK MA 3` |
| 5 | `Assembly 4` | `BACK MA 4` |
| 6 | `Assembly 5` | `BACK MA 5` |
| 7 | `Curing 1` | `CURE 1` |
| 8 | `Curing 2` | `CURE 4` |
| 9 | `Depanel 1` | `ROUTER 1` |
| 10 | `OBA 1` | `OBA 1` |
| 11 | `OBA 2` | `OBA 2` |
| 12 | `OBA 3` | `OBA 3` |
| 13 | `Progression 1` | `PRGS 1` |
| 14 | `Test 1` | `TEST 1` |
| 15 | `VMI 2` | `VMI 2` |
| 16 | `VMI 3` | `VMI 3` |
| 17 | `VMI 4` | `VMI 4` |
| 18 | `VMI 5` | `VMI 5` |
| 19 | `Wash 1` | `WASH 1` |
| 20 | `Wash 2` | `WASH 2` |
| 21 | `Wash 3` | `WASH 3` |

#### `PHOTONICS BK_3F_B37A`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1` |
| 2 | `Assembly 2` | `BACK MA 2` |
| 3 | `Assembly 3` | `BACK MA 3` |
| 4 | `Oven 1` | `BAKE 1` |
| 5 | `Oven 2` | `BAKE 2` |
| 6 | `Oven 3` | `BAKE 3` |
| 7 | `Progression 1` | `PRGS 1` |
| 8 | `Wash 1` | `WASH 1` |
| 9 | `Wash 2` | `WASH 2` |
| 10 | `Wash 3` | `WASH 3` |

#### `PHOTONICS BK_3F_B38A`  —  22 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `Assembly 1` | `FRONT MA 1` |
| 4 | `Assembly 2` | `FRONT MA 2` |
| 5 | `BSI 1` | `BSI 1` |
| 6 | `CC Cure 1` | `UF CURE 1` |
| 7 | `CC Oven 1` | `BAKE 1` |
| 8 | `CC QC 1` | `QC 1` |
| 9 | `CC QC 2` | `QC 2` |
| 10 | `FNI 1` | `FNI 1` |
| 11 | `Label 1` | `BIRTH 1` |
| 12 | `Placement BOT 1` | `SMTB 1` |
| 13 | `Placement TOP 1` | `SMTT 1` |
| 14 | `Reflow BOT 1` | `REFLOWB 1` |
| 15 | `Reflow TOP 1` | `REFLOWT 1` |
| 16 | `SCR BOT 1` | `SCRB 1` |
| 17 | `SCR TOP 1` | `SCRT 1` |
| 18 | `SPI BOT 1` | `SPIB 1` |
| 19 | `SPI TOP 1` | `SPIT 1` |
| 20 | `TSI 1` | `TSI 1` |
| 21 | `Wash 1` | `WASH 1` |
| 22 | `XRAY 1` | `XRAY 1` |


### LAMGB

#### `LGB HLA OPT BK2-1`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `SUB MA 1 - Dep Pallet assy 10` |
| 2 | `Assembly 2` | `SUB MA 1 - Dep Pallet assy 20` |
| 3 | `Assembly 3` | `SUB MA 1 - Dep Pallet assy 30` |
| 4 | `Assembly 4` | `SUB MA 1 - Dep Pallet assy 40` |
| 5 | `Assembly 5` | `MA 1 - Dep OPT 10` |
| 6 | `Assembly 6` | `MA 1 - Dep OPT 20` |
| 7 | `Assembly 7` | `MA 1 - Dep OPT 30` |
| 8 | `Assembly 8` | `MA 1 - Dep OPT 40` |
| 9 | `Assembly 9` | `FMA 1 - Dep FA 10` |
| 10 | `FNI 1` | `FNI 1 - Dep FNI 10` |
| 11 | `OBA 1` | `FQC 1 - Dep FQC 10` |
| 12 | `Packout 1` | `PACKOUT 1 - Dep Bagging` |
| 13 | `Press 1` | `PDT 1 - Dep PD` |
| 14 | `Test 1` | `FVT 1 - Dep FVT` |

#### `LGB HLA WELD BK2-1`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Cut 1` | `CUT 1 - CUTTING` |
| 2 | `Leak Test 1` | `LEAK TEST 1 - LEAK TEST` |
| 3 | `Packout 1` | `PACKOUT 1 - Bagging10` |
| 4 | `QC 1` | `WELD INSP - WELDMENT INSPECTION` |
| 5 | `Test 1` | `TWEAK TEST 1 - TWEAKING` |
| 6 | `Ultrasonic 1` | `UWASH 1 - ULTROSONIC WASH 1` |
| 7 | `Weld 1` | `TACK WELD 1 - TACK WELDING` |
| 8 | `Weld 2` | `ORBITAL WELD 1 - ORBITAL WELD` |


### LAMMEC

#### `LMECH BE PB OPT BK2-1`  —  12 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA (OPT 10)` |
| 2 | `Assembly 2` | `MA (OPT 20)` |
| 3 | `Assembly 3` | `MA (OPT 30)` |
| 4 | `Assembly 4` | `MA (OPT 40)` |
| 5 | `Assembly 5` | `MA (OPT 50)` |
| 6 | `Assembly 6` | `MA (OPT 60)` |
| 7 | `VMI 1` | `VMI (OPT 10)` |
| 8 | `VMI 2` | `VMI (OPT 20)` |
| 9 | `VMI 3` | `VMI (OPT 30)` |
| 10 | `VMI 4` | `VMI (OPT 40)` |
| 11 | `VMI 5` | `VMI (OPT 50)` |
| 12 | `VMI 6` | `VMI (OPT 60)` |

#### `LMECH BE PB PACK BK2-1`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `FA` |
| 2 | `FNI 1` | `FNI` |
| 3 | `OBA 1` | `FQC` |
| 4 | `Packout 1` | `PACKOUT` |
| 5 | `Test 1` | `TEST (VERTICAL)` |
| 6 | `Test 2` | `TEST (SMART IMAGE)` |
| 7 | `Test 3` | `TEST (PB)` |

#### `LMECH BE PB SUB BK2-1`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA (SUB 10)` |
| 2 | `Assembly 2` | `MA (SUB 30)` |
| 3 | `Assembly 3` | `MA (SUB 20)` |
| 4 | `Assembly 4` | `MA (SUB 40)` |
| 5 | `Assembly 5` | `MA (SUB 50)` |
| 6 | `Assembly 6` | `MA (SUB 60)` |


### MICRON SIG

#### `MSIG BE BIB BK2-2 B29`  —  12 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1` |
| 2 | `Assembly 3` | `BACK MA 2` |
| 3 | `FNI 2` | `FNI VIP 1` |
| 4 | `FVT 1` | `FVT (SHORT) 2` |
| 5 | `FVT 2` | `FVT (FUSE) 3` |
| 6 | `FVT 3` | `FVT (CELL) 4` |
| 7 | `Label 1` | `LABEL (BE) 1` |
| 8 | `Link 4` | `V LINK 1` |
| 9 | `OBA 2` | `OBA VIP 1` |
| 10 | `Oven 1` | `BAKE 1` |
| 11 | `Packout 1` | `PACKOUT 1` |
| 12 | `QC 1` | `PMI VIP 1` |

#### `MSIG BE DRAX BK2-2 B28`  —  12 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 2` | `BACK MA 1` |
| 2 | `Assembly 3` | `BACK MA 2` |
| 3 | `Assembly 4` | `BACK MA 3` |
| 4 | `Dispense BOT 1` | `GLUEB (TIM) 1` |
| 5 | `Dispense TOP 1` | `GLUET (TIM) 1` |
| 6 | `FVT 1` | `FVT 1` |
| 7 | `FVT 2` | `FVT 2` |
| 8 | `FVT 3` | `FVT 3` |
| 9 | `FVT 4` | `FVT 4` |
| 10 | `FVT 5` | `FVT 5` |
| 11 | `Oven 1` | `BAKE 1` |
| 12 | `QC 1` | `PMI 1` |

#### `MSIG BE PACK BK2-2 B29`  —  5 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1` |
| 2 | `FNI 2` | `FNI VIP 1` |
| 3 | `OBA 1` | `OBA 1` |
| 4 | `OBA 2` | `OBA VIP 1` |
| 5 | `Packout 1` | `PACKOUT 1` |

#### `MSIG BE SUB BK1-1 B11`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `BIRTH (SUB HLA) 1` |

#### `MSIG HLA BK1-1 B9`  —  24 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1` |
| 2 | `Assembly 10` | `HLA 7` |
| 3 | `Assembly 3` | `HLA 2` |
| 4 | `Assembly 5` | `HLA 3` |
| 5 | `Assembly 7` | `HLA 4` |
| 6 | `Assembly 8` | `HLA 5` |
| 7 | `Assembly 9` | `HLA 6` |
| 8 | `FNI 1` | `HFNI 1` |
| 9 | `FVT 1` | `FVT 1` |
| 10 | `FVT 2` | `FVT 2` |
| 11 | `FVT 3` | `FVT 3` |
| 12 | `Hi-Pot 1` | `HIPOT 1` |
| 13 | `Link 1` | `BIRTH (HLA) 1` |
| 14 | `Link 6` | `V LINK 1` |
| 15 | `OBA 1` | `HOBA 1` |
| 16 | `Packout 2` | `PACKOUT 1` |
| 17 | `QC 1` | `INSP VIP (HLA) 1` |
| 18 | `QC 2` | `INSP (HLA) 1` |
| 19 | `QC 3` | `INSP VIP (HLA) 2` |
| 20 | `QC 4` | `INSP (HLA) 2` |
| 21 | `QC 5` | `INSP VIP (HLA) 3` |
| 22 | `QC 6` | `INSP (HLA) 3` |
| 23 | `QC 7` | `INSP VIP (HLA) 4` |
| 24 | `QC 8` | `INSP (HLA) 4` |

#### `MSIG SMT BK2-2 B28`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `BSI 1` | `BSI 1` |
| 4 | `Handplace BOT 1` | `HANDPLACEB 1` |
| 5 | `Handplace TOP 1` | `HANDPLACET 1` |
| 6 | `Label 1` | `BIRTH 1` |
| 7 | `Load 1` | `LOADB 1` |
| 8 | `Load 2` | `LOADT 1` |
| 9 | `Placement BOT 1` | `SMTB 1` |
| 10 | `Placement TOP 1` | `SMTT 1` |
| 11 | `Reflow BOT 1` | `REFLOWB 1` |
| 12 | `Reflow TOP 1` | `REFLOWT 1` |
| 13 | `SCR BOT 1` | `SCRB 1` |
| 14 | `SCR TOP 1` | `SCRT 1` |
| 15 | `SPI BOT 1` | `SPIB 1` |
| 16 | `SPI TOP 1` | `SPIT 1` |
| 17 | `TSI 1` | `TSI 1` |

#### `MSIG TH BK2-2 B28`  —  31 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `(no alias)` |
| 2 | `Depanel 1` | `ROUTER 1` |
| 3 | `FNI 1` | `FNI 1` |
| 4 | `FNI 2` | `HFNI 1` |
| 5 | `FNI 3` | `XHFNI 1` |
| 6 | `ICT 1` | `FPROBEB 1` |
| 7 | `ICT 2` | `FPROBET 1` |
| 8 | `ICT 3` | `FPROBE 1` |
| 9 | `Link 2` | `(no alias)` |
| 10 | `Link 3` | `(no alias)` |
| 11 | `Link 4` | `(no alias)` |
| 12 | `MI 1` | `CHEMASK 1` |
| 13 | `MI 2` | `MIB 1` |
| 14 | `MI 3` | `MIT 1` |
| 15 | `OBA 1` | `OBA 1` |
| 16 | `Packout 1` | `PACKOUT 1` |
| 17 | `Press 1` | `PRESS FITB 1` |
| 18 | `Press 2` | `PRESS FITT 1` |
| 19 | `Press 3` | `PRESS FIT 1` |
| 20 | `Program 1` | `(no alias)` |
| 21 | `Selective 1` | `S WAVET 1` |
| 22 | `Solder 1` | `M SOLDER 1` |
| 23 | `THI 1` | `TSTHB 1` |
| 24 | `THI 2` | `TSTHT 1` |
| 25 | `Touch Up 1` | `PWTUB 1` |
| 26 | `Touch Up 2` | `PWTUT 1` |
| 27 | `Wash 2` | `WASH 2` |
| 28 | `Wash 3` | `WASH 3` |
| 29 | `Wave 1` | `C WAVEB 1` |
| 30 | `Wave 2` | `C WAVET 1` |
| 31 | `XRAY 1` | `XRAY 1` |

#### `MSIG TH BK2-2 B29`  —  26 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB (BE) 1` |
| 2 | `Assembly 1` | `FRONT MA 1` |
| 3 | `Assembly 2` | `MA (TORQUE) 1` |
| 4 | `Auto Insert 1` | `AI 1` |
| 5 | `BSI 1` | `BSI (BE) 1` |
| 6 | `FNI 1` | `FNI (AOP) 1` |
| 7 | `FNI 2` | `FNI (AOP) 2` |
| 8 | `Link 1` | `LINK (FRONT MA) 1` |
| 9 | `Link 2` | `LINK (MI) 1` |
| 10 | `Link 3` | `LINK (AOP) 1` |
| 11 | `Link 4` | `LINK (AOP) 2` |
| 12 | `MI 2` | `MIT 1` |
| 13 | `Mask 1` | `MASKB 1` |
| 14 | `Oven 1` | `OVEN 1` |
| 15 | `Press 1` | `PRESS FIT (MEP) 1` |
| 16 | `QC 1` | `INSP (AI) 1` |
| 17 | `THI 1` | `PRE MI 1` |
| 18 | `THI 2` | `TSTHB 1` |
| 19 | `Touch Up 1` | `PWTU 1` |
| 20 | `Wash 1` | `WASH 1` |
| 21 | `Wash 2` | `WASH 2` |
| 22 | `Wash 3` | `WASH 3` |
| 23 | `Wave 1` | `C WAVET 1` |
| 24 | `XRAY 1` | `XRAY 1` |
| 25 | `XRAY 2` | `XRAY 2` |
| 26 | `XRAY 3` | `XRAY 3` |


### Masimo

#### `MAS BE PACK P1A-1 B10b`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - FNI` |
| 2 | `OBA 1` | `OBA 1 - OQA` |
| 3 | `Packout 1` | `PACKOUT  - PACKOUT` |

#### `MAS BE TEST P1A-1 B11b`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1 - BACK MECH ASSY 1` |
| 2 | `FVT 1` | `FVT 2 - FVT 2` |
| 3 | `Test 1` | `TEST (TURN ON) 1 - Turn-On Test` |
| 4 | `VMI 1` | `VMI 1 - VMI` |

#### `MAS SMT P1A-1 B11a`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1  - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIB 1  - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Label 1` | `BIRTH 1  - BIRTH` |
| 5 | `Placement BOT 1` | `SMTB 1  - SMTB01` |
| 6 | `Placement TOP 1` | `SMTB 1  - SMTT01` |
| 7 | `Reflow BOT 1` | `REFLOWB 1  - REFLOW SOLDERING BTM` |
| 8 | `Reflow TOP 1` | `REFLOWB 1  - REFLOW SOLDERING TOP` |
| 9 | `SCR BOT 1` | `SCRB 1  - SCRB01` |
| 10 | `SCR TOP 1` | `SCRB 1  - SCRT01` |
| 11 | `SPI BOT 1` | `SPIB 1  - SPI BTM` |
| 12 | `SPI TOP 1` | `SPIB 1  - SPI TOP` |
| 13 | `TSI 1` | `TSI 1 - TSI` |

#### `MAS TH FPROBE P1A-1 B9a`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ICT 1` | `FPROBET 1  - TAKAYA_T` |
| 2 | `ICT 2` | `FPROBEB 1  - TAKAYA_B` |

#### `MAS TH P1A-1 B11b`  —  5 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `MIT 1  - MI TOP LINK` |
| 2 | `Link 2` | `PWTUT 1  - LINK (SOLDER WIRE)` |
| 3 | `MI 1` | `MIT 1  - MI TOP 1` |
| 4 | `Touch Up 1` | `PWTUT 1  - PWTU TOP` |
| 5 | `Wave 1` | `CWAVET 1 - CONVENTIONAL WAVE SOLDERING TOP` |

#### `MAS TH WASH P1A-1 B11b`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER 1  - DEPANELING` |
| 2 | `ICT 1` | `ICT 1 - ICT` |
| 3 | `Link 1` | `WASHB 1  - WASH BTM LINK` |
| 4 | `Link 2` | `WASHT 1  - WASH TOP LINK` |
| 5 | `QC 1` | `POST WASH 1 - POST WASH 1 INSP` |
| 6 | `Solder 1` | `MSOLDER 1 - M.SOLDERING` |
| 7 | `THI 1` | `TSTH 1  - TSTH1` |
| 8 | `THI 2` | `TSTH 1  - TSTH TOP` |
| 9 | `Wash 1` | `WASHB 1 - WASH BTM` |
| 10 | `Wash 2` | `WASHT 1  - WASH TOP` |

#### `MAS TH XRAY P1A-1 B8b`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `XRAY 1` | `XRAY 1  - XRAY 1` |


### Medtronic

#### `MDT BE P1A-1 B12a`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 2` | `BACK MA 2 - BACK MECH ASSY 1` |
| 2 | `Cut 1` | `TSTH 1 - CUTTING` |
| 3 | `Depanel 1` | `LROUTER 1 - LASER DEPANELING` |
| 4 | `FNI 1` | `FNI 1 - FNI` |
| 5 | `FVT 1` | `FVT 1 - PROGRAMMING` |
| 6 | `FVT 2` | `FVT (FUNTIONAL TEST) 2 - FVT (FUNTIONAL TEST)` |
| 7 | `FVT 3` | `FVT (RF) 3 - FVT RF` |
| 8 | `FVT 4` | `FVT (BATTERY CHARGING) 4 - FVT 2` |
| 9 | `FVT 5` | `PTR FVT 1 - FVT` |
| 10 | `FVT 6` | `PTR FVT (TRIM & CAL) 1 - FVT TRIM AND CALIBRATION` |
| 11 | `OBA 1` | `OBA 1 - OQA` |
| 12 | `Packout 1` | `PACKOUT - PACKOUT` |
| 13 | `Press 1` | `APFIT 1 - AUTO PRESS 1` |
| 14 | `QC 1` | `BACK MA 2 - PMI` |
| 15 | `Solder 1` | `LSOLDER 1 - LASER SOLDERING` |
| 16 | `THI 1` | `TSTH 1 - TSTH` |
| 17 | `Weld 1` | `LWELD 1 - LASER WELDING 1` |

#### `MDT BE P1A-1 B9b`  —  31 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1/2 - SMART TORQUE 2` |
| 2 | `Assembly 2` | `MA 1/2 - BACK MECH ASSY 1` |
| 3 | `Assembly 3` | `MA 1/2 - BACK MECH ASSY 2` |
| 4 | `Assembly 4` | `MA 3/4 - BACK MECH ASSY 3` |
| 5 | `Assembly 5` | `MA 3/4 - BACK MECH ASSY 4` |
| 6 | `CC Cure 1` | `CURE 1 - REFLOW OVEN CURING TOP` |
| 7 | `CC Cure 2` | `MA 1/2 - ROOM TEMP CURING` |
| 8 | `Cut 1` | `CUT 1 - CUTTING` |
| 9 | `Dispense 1` | `UF 1 - UNDER FILL` |
| 10 | `Dispense 2` | `MA 1/2 - RTV GLUE` |
| 11 | `FNI 1` | `FNI 1 - FNI` |
| 12 | `FVT 1` | `FVT (STACK) 1 - FVT 1` |
| 13 | `Link 1` | `MI 1 - MI LINK` |
| 14 | `Link 2` | `CUT 1 - PWTU LINK` |
| 15 | `Link 3` | `MA 1/2 - BACK MA 1 LINK` |
| 16 | `Link 4` | `MA 1/2 - BACK MA 2 LINK` |
| 17 | `Link 5` | `MA 1/2 - LINK` |
| 18 | `Link 6` | `MA 3/4 - BACK MA 3 LINK` |
| 19 | `Link 7` | `MA 3/4 - BACK MA 4 LINK` |
| 20 | `MI 1` | `MI 1 - MI 1` |
| 21 | `OBA 1` | `OBA 1 - OQA` |
| 22 | `Oven 1` | `BAKE 1 - BAKING PCBA` |
| 23 | `Packout 1` | `PACKOUT - PACKOUT` |
| 24 | `QC 1` | `UF 1 - UNDERFILL INSPECTION` |
| 25 | `QC 2` | `POST UF INSP - POST UNDERFILL INSPECTION` |
| 26 | `QC 3` | `MA 1/2 - PMI` |
| 27 | `QC 4` | `MA 1/2 - GLUE INSPECTION` |
| 28 | `Selective 1` | `SWAVE 1 - SELECTIVE WAVE SOLDERING 1` |
| 29 | `THI 1` | `TSTH 1 - TSTH` |
| 30 | `Touch Up 1` | `CUT 1 - PWTU` |
| 31 | `VMI 1` | `VMI 1 - VMI` |

#### `MDT SMT P1A-1 B12a`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Label 1` | `LMARKER 1 - LASER MARKER` |

#### `MDT SMT P1A-1 B8a`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Birth 1` | `LABEL 1 - BIRTH` |
| 5 | `Dispense BOT 1` | `GLUEB 1 - Glue Dispenser BOT` |
| 6 | `Label 1` | `LABEL 1 - LABELING` |
| 7 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 8 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 9 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 10 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 11 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 12 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 13 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 14 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 15 | `TSI 1` | `TSI 1 - TSI` |

#### `MDT TH P1A-1 B11b`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MI 1 - SMART TORQUE 1` |
| 2 | `Link 1` | `MI 1 - MI LINK` |
| 3 | `Link 2` | `PWTU 1 - PWTU LINK` |
| 4 | `MI 1` | `MI 1 - MI 1` |
| 5 | `THI 1` | `TSTH 1 - TSTH` |
| 6 | `Touch Up 1` | `PWTU 1 - PWTU` |
| 7 | `Wave 1` | `CWAVE 1 - CONVENTIONAL WAVE SOLDERING 1` |

#### `MDT TH P1A-1 B12a`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Solder 1` | `MSOLDER 1 - MANUAL SOLDER 1` |
| 2 | `Solder 2` | `MSOLDER 2 - MANUAL SODLER 2` |

#### `MDT TH P1A-1 B6b`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Test 1` | `TEST (IONIC) 1 - IONIC TEST` |

#### `MDT TH P1A-1 B9a`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ICT 1` | `ICT 1 - ICT` |
| 2 | `ICT 2` | `FPROBE 1 - FLYING PROBE` |
| 3 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `MDT TH P1A-1 B9b`  —  16 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `CC Cure 1` | `CURE 1 - LOCTITE CURING` |
| 2 | `Depanel 1` | `ROUTER 1 - DEPANELING` |
| 3 | `Dispense 1` | `GLUE 1 - LOCTITE DISPENSING` |
| 4 | `FVT 1` | `FVT (BOARD) 1 - FVT` |
| 5 | `FVT 2` | `FVT (BOARD) 2 - FVT` |
| 6 | `Label 1` | `LABEL OUT 1 - LABELLING 1` |
| 7 | `Link 1` | `PRE WASH 1 - WASH 1 LINK` |
| 8 | `Link 2` | `PRE WASH 2 - WASH 2 LINK` |
| 9 | `Link 3` | `LABEL OUT 1 - LINK` |
| 10 | `Link 4` | `PRE WASH 3 - WASH 3 LINK` |
| 11 | `QC 1` | `POST WASH INSP 1 - POST WASH 1 INSP` |
| 12 | `QC 2` | `POST WASH INSP 2 - POST WASH 2 INSP` |
| 13 | `QC 3` | `LABEL OUT 1 - LABEL INSPECTION` |
| 14 | `Wash 1` | `WASH 1 - CHEMICAL WASH 1` |
| 15 | `Wash 2` | `WASH 2 - CHEMICAL WASH 2` |
| 16 | `Wash 3` | `WASH 3 - WASH 3` |


### Motorola

#### `MOTOROLA BE B_34 2F`  —  19 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1` |
| 2 | `Assembly 10` | `HLA 10` |
| 3 | `Assembly 2` | `HLA 2` |
| 4 | `Assembly 3` | `HLA 3` |
| 5 | `Assembly 4` | `HLA 4` |
| 6 | `Assembly 5` | `HLA 5` |
| 7 | `Assembly 6` | `HLA 6` |
| 8 | `Assembly 7` | `HLA 7` |
| 9 | `Assembly 8` | `HLA 8` |
| 10 | `Assembly 9` | `HLA 9` |
| 11 | `FNI 1` | `HFNI 1` |
| 12 | `Label 1` | `Birth 1` |
| 13 | `Label 2` | `LABEL (COMPRO) 1` |
| 14 | `Packout 1` | `PACKOUT 1` |
| 15 | `Program 1` | `PROG (NL BRD) 1` |
| 16 | `Test 1` | `TEST (NL BEST ) 1` |
| 17 | `Test 2` | `TEST (NL CIT) 1` |
| 18 | `Test 3` | `TEST (NL COMPRO) 1` |
| 19 | `Test 4` | `TEST (NL SNC) 1` |

#### `MOTOROLA BE B_34B 2F`  —  23 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `HLA 1` |
| 2 | `Assembly 10` | `HLA 10` |
| 3 | `Assembly 11` | `HLA 11` |
| 4 | `Assembly 12` | `HLA 12` |
| 5 | `Assembly 13` | `HLA 13` |
| 6 | `Assembly 14` | `HLA 14` |
| 7 | `Assembly 2` | `HLA 2` |
| 8 | `Assembly 3` | `HLA 3` |
| 9 | `Assembly 4` | `HLA 4` |
| 10 | `Assembly 5` | `HLA 5` |
| 11 | `Assembly 6` | `HLA 6` |
| 12 | `Assembly 7` | `HLA 7` |
| 13 | `Assembly 8` | `HLA 8` |
| 14 | `Assembly 9` | `HLA 9` |
| 15 | `FNI 1` | `HFNI 1` |
| 16 | `Packout 1` | `PACKOUT 1` |
| 17 | `Program 1` | `PROG (RAJ BOARD) 1` |
| 18 | `Test 1` | `TEST (RAJ WIRELESS) 1` |
| 19 | `Test 2` | `TEST (RAJ LEAK) 1` |
| 20 | `Test 3` | `TEST (RAJS BEST) 1` |
| 21 | `Test 4` | `TEST (RAJS ATS) 1` |
| 22 | `Test 5` | `TEST (RAJ CIT) 1` |
| 23 | `Test 6` | `TEST (RAJ SNC) 1` |

#### `MOTOROLA B_34 2F`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `PRE AOIB 1` |
| 2 | `AOI BOT 2` | `AOIB 1` |
| 3 | `AOI TOP 1` | `PRE AOIT 1` |
| 4 | `AOI TOP 2` | `AOIT 1` |
| 5 | `BSI 1` | `BSI 1` |
| 6 | `Handplace TOP 1` | `HANDPLACET 1` |
| 7 | `Label 1` | `BIRTH 1` |
| 8 | `Placement BOT 1` | `SMTB 1` |
| 9 | `Placement TOP 1` | `SMTT 1` |
| 10 | `Placement TOP 2` | `SMTT 2` |
| 11 | `Reflow BOT 1` | `REFLOWB 1` |
| 12 | `Reflow TOP 1` | `REFLOWT 1` |
| 13 | `SCR BOT 1` | `SCRB 1` |
| 14 | `SCR TOP 1` | `SCRT 1` |
| 15 | `SPI BOT 1` | `SPIB 1` |
| 16 | `SPI TOP 1` | `SPI TOP 1` |
| 17 | `TSI 1` | `TSI 1` |

#### `MSI BALI TAHITI SUB`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `SUB ASSY 1` |


### Nokia Optics

#### `ADVA BE PACKOUT 3F`  —  2 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Packout 1` | `(no alias)` |
| 2 | `QC 1` | `(no alias)` |

#### `NOKIA BE 3F`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 2` | `MA 1` |
| 2 | `Assembly 3` | `MA (THERMAL GEL) 1` |
| 3 | `Assembly 5` | `MA 3` |
| 4 | `FVT 1` | `FVT (OFCT) 1` |
| 5 | `Link 1` | `LINK (COMBO) 1` |
| 6 | `Link 2` | `PACKOUT 1` |
| 7 | `Oven 1` | `BAKE 1` |
| 8 | `QC 1` | `HLA INSP 1` |
| 9 | `QC 3` | `VMI 2` |
| 10 | `QC 4` | `OBA1` |
| 11 | `QC 5` | `PRE FVT INSP (OPTIC) 1` |
| 12 | `QC 7` | `FNI 1` |
| 13 | `QC 8` | `OBA 1` |

#### `NOKIA EMA 3F`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1` |
| 2 | `Assembly 2` | `XRAY 1` |
| 3 | `Assembly 3` | `SPLICE (OPTIC) 1` |
| 4 | `Link 1` | `LINK (COMBO) 1` |
| 5 | `Link 2` | `PACK VER 1` |
| 6 | `QC 2` | `PRE FVT INSP (OPTIC) 1` |
| 7 | `QC 3` | `POST FVT INSP (OPTIC) 1` |
| 8 | `QC 4` | `VMI 1` |
| 9 | `Solder 1` | `ASOLDER (HOTBAR) 1` |
| 10 | `Solder 2` | `MSOLDER 1` |

#### `NOKIA HLA 3F`  —  25 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `ASOLDERB (HOTBAR) 1` |
| 2 | `Assembly 10` | `(no alias)` |
| 3 | `Assembly 2` | `ASOLDERT (HOTBAR) 1` |
| 4 | `Assembly 3` | `PUNCH 1` |
| 5 | `Assembly 4` | `BAKE 1` |
| 6 | `Assembly 5` | `(no alias)` |
| 7 | `Assembly 6` | `(no alias)` |
| 8 | `Assembly 7` | `(no alias)` |
| 9 | `Assembly 8` | `(no alias)` |
| 10 | `Assembly 9` | `(no alias)` |
| 11 | `FVT 1` | `(no alias)` |
| 12 | `Link 1` | `LINK (COMBO) 1` |
| 13 | `Link 2` | `LINK 3` |
| 14 | `Link 3` | `PACK VER 1` |
| 15 | `Link 4` | `(no alias)` |
| 16 | `QC 1` | `PMI 1` |
| 17 | `QC 2` | `VMI 1` |
| 18 | `QC 4` | `(no alias)` |
| 19 | `QC 5` | `(no alias)` |
| 20 | `QC 6` | `OBA 1` |
| 21 | `QC 7` | `(no alias)` |
| 22 | `QC 8` | `(no alias)` |
| 23 | `Solder 1` | `MSOLDER 1` |
| 24 | `Test 2` | `XRAY 1` |
| 25 | `Test 3` | `(no alias)` |

#### `NOKIA SUB 3F`  —  6 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PREP (OPTIC) 1` |
| 2 | `Link 1` | `LINK (COMBO) 1` |
| 3 | `Link 2` | `PACK VER 1` |
| 4 | `QC 1` | `VMI 1` |
| 5 | `QC 2` | `OBA 1` |
| 6 | `Solder 1` | `MSOLDER (OPTIC) 1` |

#### `PHOTONICS BK_3F_B31A`  —  20 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `BSI 1` | `BSI 1` |
| 4 | `Depanel 1` | `ROUTER 1` |
| 5 | `Depanel 2` | `ROUTER 2` |
| 6 | `Handplace TOP 1` | `HPLACET 1` |
| 7 | `ICT 1` | `ICT 1` |
| 8 | `Label 1` | `BIRTH 1` |
| 9 | `Label 2` | `BIRTH 2` |
| 10 | `MI 1` | `MI 1` |
| 11 | `Placement BOT 1` | `SMTB 1` |
| 12 | `Placement TOP 1` | `SMTT 1` |
| 13 | `Reflow BOT 1` | `REFLOWB 1` |
| 14 | `Reflow TOP 1` | `REFLOWT 1` |
| 15 | `SCR BOT 1` | `SCRB 1` |
| 16 | `SCR TOP 1` | `SCRT 1` |
| 17 | `SPI BOT 1` | `SPIB 1` |
| 18 | `SPI TOP 1` | `SPIT 1` |
| 19 | `TSI 1` | `TSI 1` |
| 20 | `Touch Up 1` | `PWTU 1` |

#### `PHOTONICS SMT B_5a`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1` |
| 2 | `AOI TOP 1` | `AOIT 1` |
| 3 | `Handplace TOP 1` | `HPLACET 1` |
| 4 | `Label 1` | `BIRTH 1` |
| 5 | `Placement BOT 1` | `SMTB 1` |
| 6 | `Placement TOP 1` | `SMTT 1` |
| 7 | `Reflow BOT 1` | `REFLOWB 1` |
| 8 | `Reflow TOP 1` | `REFLOWT 1` |
| 9 | `SCR BOT 1` | `SCB 1` |
| 10 | `SCR TOP 1` | `SCRT 1` |
| 11 | `SPI BOT 1` | `SPB 1` |

#### `PHOTONICS TH B_12a`  —  5 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ICT 1` | `ICT 1` |
| 2 | `Link 1` | `LINK 1` |
| 3 | `QC 1` | `QC 1` |
| 4 | `XRAY 2` | `XRAY 2` |
| 5 | `XRAY 3` | `XRAY 3` |


### ResMed

#### `RMD BE P1A-1 B7`  —  8 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AVI 1` | `AVI 1 - AVI` |
| 2 | `Assembly 1` | `MA 2 - BACK MECH ASSY 1` |
| 3 | `FNI 1` | `FNI 1 - FNI` |
| 4 | `OBA 1` | `OBA 1 - OQA` |
| 5 | `Packout 1` | `PACKOUT  - PACKOUT` |
| 6 | `Test 1` | `TEST (C TUNE) 1 - FVT Ctune` |
| 7 | `Test 2` | `TEST (NON RF) 1 - FVT Non RF` |
| 8 | `Test 3` | `TEST (RF) 1 - FVT RF` |

#### `RMD BE P1A-1 B8`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - FNI` |
| 2 | `OBA 1` | `OBA 1 - OQA` |
| 3 | `Packout 1` | `PACKOUT  - PACKOUT` |

#### `RMD BE P1A-1 B9`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FVT 1` | `FVT 1 - FVT` |

#### `RMD SMT P1A-1 B7`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 5 | `Dispense TOP 1` | `GLUET 1 - GLUE TOP` |
| 6 | `Label 1` | `BIRTH 1 - LABELING` |
| 7 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 8 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 9 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 10 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 11 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 12 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 13 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 14 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 15 | `TSI 1` | `TSI 1 - TSI` |

#### `RMD SMT P1A-1 B8`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 5 | `Dispense BOT 1` | `GLUEB 1 - GLUE DISPENSING BTM` |
| 6 | `Label 1` | `BIRTH 1 - LABELING` |
| 7 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 8 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 9 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 10 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 11 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 12 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 13 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 14 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 15 | `TSI 1` | `TSI 1 - TSI` |

#### `RMD TH P1A-1 B7`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `FRONT MA 1 - FRONT MECH ASSY 1` |
| 2 | `Assembly 4` | `FRONT MA 2 - FRONT MECH ASSY 2` |
| 3 | `Depanel 1` | `ROUTER 1 - Depanel` |
| 4 | `ICT 1` | `ICT 1 - ICT` |
| 5 | `QC 1` | `POST XRAY 1 - XRAY` |
| 6 | `Solder 2` | `ASOLDER 1 - ROBOTIC SOLDERING BTM 1` |
| 7 | `THI 1` | `TSTH 1 - TSTH` |
| 8 | `Touch Up 1` | `PWTU 1 - PWTU BTM` |
| 9 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `RMD TH P1A-1 B9`  —  7 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `POST XRAY 1 - XRAY` |
| 2 | `Assembly 2` | `MA 1 - BACK MECH ASSY 1` |
| 3 | `Depanel 1` | `ROUTER 1 - Depanel` |
| 4 | `ICT 1` | `ICT 1 - ICT` |
| 5 | `Solder 1` | `MSOLDER (HOTB) 1 - M. SOLDERING 1` |
| 6 | `THI 1` | `TSTH 1- TSTH` |
| 7 | `XRAY 1` | `XRAY 1 - XRAY` |


### TMO

#### `TMO BE P1B-2 B8a`  —  12 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1 - BACK MECH ASSY 1` |
| 2 | `Assembly 2` | `MA 2 - Mech Assy2` |
| 3 | `Assembly 3` | `MA 3 - Mech Assy3` |
| 4 | `FVT 1` | `FVT 1 - FVT` |
| 5 | `FVT 2` | `FVT 2 - FVT 1` |
| 6 | `FVT 3` | `FVT 3 - FVT 2` |
| 7 | `Link 1` | `BACK MA 1 - BACK MA 1 LINK` |
| 8 | `Link 2` | `M SOLDER 1 - M.SOLDER 1 LINK` |
| 9 | `Link 3` | `M SOLDER 2 - M.SOLDER 2 LINK` |
| 10 | `Potting 1` | `POT 1 - POTTING` |
| 11 | `Solder 1` | `M SOLDER 1 - M.SOLDERING 1` |
| 12 | `Solder 2` | `M SOLDER 2 - M.SOLDERING 2` |

#### `TMO BE P1B-2 B8b`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `FNI 1 - FNI` |
| 2 | `Link 1` | `PACKOUT 1 - PACKOUT LINK` |
| 3 | `OBA 1` | `OBA 1 - OQA` |
| 4 | `Packout 1` | `PACKOUT 1 - PACKOUT` |

#### `TMO HLA P1B-2 C1`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `MA 1 - HLA MECH ASSY 1` |
| 2 | `Assembly 2` | `MA 1 - SMART TORQUE 1` |
| 3 | `Assembly 3` | `MA 2 - HLA MECH ASSY 2` |
| 4 | `Assembly 4` | `MA 2 - SMART TORQUE 2` |
| 5 | `Assembly 5` | `MA 3 - HLA MECH ASSY 3` |
| 6 | `Assembly 6` | `MA 3 - SMART TORQUE 3` |
| 7 | `Birth 1` | `PRE TEST 1 - BIRTH_01` |
| 8 | `Hi-Pot 1` | `HIPOT 1 - HIPOT` |
| 9 | `Link 1` | `MA 1 - HLA 1 LINK` |
| 10 | `Link 2` | `MA 2 - HLA 2 LINK` |
| 11 | `Link 3` | `MA 3 - HLA 3 LINK` |
| 12 | `QC 1` | `MA INSP 1 - HLA MAI 1` |
| 13 | `QC 2` | `MA INSP 2 - HLA MAI 2` |

#### `TMO HLA P1B-2 C2`  —  9 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FNI 1` | `HFNI 1 - HFNI VIP` |
| 2 | `FNI 2` | `FNI 1 - HFNI` |
| 3 | `Link 1` | `PACKOUT 1 - HLAPACKOUT LINK` |
| 4 | `OBA 1` | `OBA 1 - HOQA VIP` |
| 5 | `OBA 2` | `OBA 1 - HOQA` |
| 6 | `Packout 1` | `PACKOUT 1 - PACKOUT` |
| 7 | `Test 1` | `SYSTEM TEST 1 - SYSTEM TEST` |
| 8 | `Test 2` | `SYSTEM TEST 2 - SYSTEM TEST 1` |
| 9 | `Test 3` | `SYSTEM TEST 3 - SYSTEM TEST 2` |

#### `TMO SMT P1A-1 B14a`  —  18 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Birth 1` | `BIRTH 1 - BIRTH` |
| 5 | `Dispense BOT 1` | `GLUEB 1 - GLUEB01` |
| 6 | `Dispense TOP 1` | `GLUET 1 - GLUET01` |
| 7 | `Handplace BOT 1` | `HPLACEB 1 - MANUAL ONSERT BTM` |
| 8 | `Handplace TOP 1` | `HPLACET 1 - MANUAL ONSERT TOP` |
| 9 | `Label 1` | `BIRTH 1 - LABELING` |
| 10 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 11 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 12 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 13 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 14 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 15 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 16 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 17 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 18 | `TSI 1` | `TSI 1 - TSI` |

#### `TMO TH P1A-1 B13b`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ICT 1` | `ICT 1 - ICT` |
| 2 | `ICT 2` | `FPROBET 1 - FLYING PROBE TOP` |
| 3 | `ICT 3` | `FPROBEB 1 - FLYING PROBE BTM` |
| 4 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `TMO TH P1A-1 B14b`  —  16 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `DEPANEL 1 - DEPANELING` |
| 2 | `Link 1` | `WASH 1 - WASH 1 LINK` |
| 3 | `Link 2` | `MI 1 - MI TOP LINK` |
| 4 | `Link 3` | `MI 1 - MI BTM LINK` |
| 5 | `Link 4` | `PWTU 1 - PWTU TOP LINK` |
| 6 | `Link 5` | `PWTU 1 - PWTU BTM LINK` |
| 7 | `MI 1` | `MI 1 - MI TOP 1` |
| 8 | `MI 2` | `MI 1 - MI BTM 1` |
| 9 | `Press 1` | `PRESS FIT 1 - PRESS FIT 1` |
| 10 | `QC 1` | `POST WASH INSP 1 - Post Wash 1 Insp` |
| 11 | `THI 1` | `TSTH 1 - TSTH` |
| 12 | `Touch Up 1` | `PWTU 1 - PWTU TOP` |
| 13 | `Touch Up 2` | `PWTU 1 - PWTU BTM` |
| 14 | `Wash 1` | `WASH 1 - Wash1` |
| 15 | `Wave 1` | `CWAVE 1 - CONVENTIONAL WAVE SOLDERING TOP` |
| 16 | `Wave 2` | `CWAVE 1 - CONVENTIONAL WAVE SOLDERING BTM` |


### UTAS

#### `UTAS CC P1B-2`  —  41 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE MI (SCREW) 1 - Manual PRE-MI` |
| 2 | `Assembly 2` | `MA 1 - Assemble Mech Assy1` |
| 3 | `Assembly 3` | `MA 1 - SMART TORQUE SMART TORQUE 1` |
| 4 | `Assembly 4` | `MA 2 - Assemble Mech Assy2` |
| 5 | `Assembly 5` | `MA 2 - SMART TORQUE SMART TORQUE 2` |
| 6 | `Bonding 1` | `BOND 1 - Assemble BONDING 1` |
| 7 | `Bonding 2` | `BOND 2  - Assemble BONDING 2` |
| 8 | `CC Cure 1` | `CUREB 1 - CURING Curing Bot` |
| 9 | `CC Cure 2` | `STAGEB 1 - Assemble Staging Bot` |
| 10 | `CC Cure 3` | `CURET 1 - CURING CURING TOP` |
| 11 | `CC Cure 4` | `STAGET 1 - Assemble Stanging Top` |
| 12 | `CC Oven 1` | `BAKE 1 - BAKING BAKING1` |
| 13 | `CC QC 1` | `INSPB (PRE COAT) 1 - QC PRE COATING INSP BTM` |
| 14 | `CC QC 2` | `INSPT (PRE COAT) 1 - QC PRE COATING INSP TOP` |
| 15 | `CC QC 3` | `INSPB (POST COAT) 1 - QC POST COATING INSP BTM` |
| 16 | `CC QC 4` | `INSPT (POST COAT) 1 - QC POST COATING INSP TOP` |
| 17 | `CC Spray 1` | `COATB 1 - COATING Coating Bot` |
| 18 | `CC Spray 2` | `COATT 1 - COATING Coating Top` |
| 19 | `CC Touch Up 1` | `TU (COATB1) 1 - Assemble Coating Touch up` |
| 20 | `CC Touch Up 2` | `TU (COATT1) 1 - COATING TOUCH COAT` |
| 21 | `Curing 1` | `CURE 1 - CURING CURING` |
| 22 | `Curing 2` | `CURE (EPOXY) 1 - CURING EPOXY CURING 1` |
| 23 | `Curing 3` | `CURE 2 - CURING CURING 2` |
| 24 | `Curing 4` | `CURE (EPOXY) 2 - CURING EPOXY CURING 2` |
| 25 | `De-Mask 1` | `UNMASKB 1 - Assemble DE-Masking Bot` |
| 26 | `De-Mask 2` | `UNMASKT 1 - Assemble DE- Masking Top` |
| 27 | `ESS 1` | `ESS 1 - FVT ESS` |
| 28 | `FNI 1` | `FNI VIP 1 - QC FNI1_VIP` |
| 29 | `FNI 2` | `FNI VIP 2 - QC FNI2_VIP` |
| 30 | `FVT 1` | `FVT 1 - FVT FVT1` |
| 31 | `FVT 2` | `FVT 2 - FVT FVT2` |
| 32 | `FVT 3` | `FVT 3 - FVT FVT3` |
| 33 | `Mask 1` | `MASK 1 - Assemble MASKING 1 BOT & TOP` |
| 34 | `OBA 1` | `OBA VIP 1 - QC OQA1_VIP` |
| 35 | `OBA 2` | `OBA VIP 2 - QC OQA2_VIP` |
| 36 | `Packout 1` | `PACKOUT  - PACKOUT PACKOUT` |
| 37 | `Solder 1` | `M SOLDER 1 - Assemble Manual Soldering 1 # 1` |
| 38 | `Solder 2` | `M SOLDER 2 - Assemble Manual Soldering 1 # 2` |
| 39 | `Solder 3` | `M SOLDER 3 - Assemble Manual Soldering 1 # 3` |
| 40 | `Test 1` | `TEST (BSCAN) 1 - AUTOTEST BOUNDARY SCAN 1` |
| 41 | `Test 2` | `TEST (BSCAN) 2 - AUTOTEST BOUNDARY SCAN 2` |

#### `UTAS SMT P1A-1 B5a`  —  15 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - QC BSI` |
| 4 | `Dispense BOT 1` | `GLUEB 1 - Glue GLUEB01` |
| 5 | `Dispense TOP 1` | `GLUET 1 - Glue GLUET01` |
| 6 | `Label 1` | `BIRTH 1 - LABEL` |
| 7 | `Placement BOT 1` | `SMTB 1 - SMT SMTB01` |
| 8 | `Placement TOP 1` | `SMTT 1 - SMT SMTT01` |
| 9 | `Reflow BOT 1` | `REFLOWB 1 - Oven REFLOW SOLDERING BTM` |
| 10 | `Reflow TOP 1` | `REFLOWT 1 - Oven REFLOW SOLDERING TOP` |
| 11 | `SCR BOT 1` | `SCRB 1 - SCR SCRB01` |
| 12 | `SCR TOP 1` | `SCRT 1 - SCR SCRT01` |
| 13 | `SPI BOT 1` | `SPIB 1 - SPI BTM 1` |
| 14 | `SPI TOP 1` | `SPIT 1 - SMT SPI TOP` |
| 15 | `TSI 1` | `TSI 1 - QC TSI` |

#### `UTAS TH P1A-1 B5b`  —  21 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE PWTU 1 - QC Pre PWTU 1` |
| 2 | `Assembly 2` | `PRE PWTU 2 - QC Pre PWTU 2` |
| 3 | `Depanel 1` | `ROUTER 1 - Router Router` |
| 4 | `ICT 1` | `FPROBE 1 - AUTOTEST TAKAYA_AUTO` |
| 5 | `ICT 2` | `ICT 1 - ICT ICT` |
| 6 | `Link 1` | `MI 1 - LINK MI1` |
| 7 | `Link 2` | `MI 2 - LINK MI2` |
| 8 | `Link 3` | `EPTST 1 - LINK EPTS TOP` |
| 9 | `Link 4` | `EPTSB 1 - LINK EPTS BTM` |
| 10 | `MI 1` | `MI 1 - Assemble MI_1` |
| 11 | `MI 2` | `MI 2 - Assemble MI_2` |
| 12 | `Selective 1` | `S WAVE 1 - WAVE SELECTIVE WAVE` |
| 13 | `THI 1` | `TSTH 1 - QC TSTH` |
| 14 | `Test 1` | `TEST (IONIC) 1 - Manual Test IONIC TEST 1` |
| 15 | `Test 2` | `TEST (IONIC) 2 - Manual Test IONIC TEST 2` |
| 16 | `Test 3` | `TEST (IONIC) 3 - Manual Test IONIC TEST 3` |
| 17 | `Test 4` | `TEST (IONIC) 4 - Manual Test IONIC TEST 4` |
| 18 | `Touch Up 1` | `PWTU 1 - QC PWTU1` |
| 19 | `Touch Up 2` | `PWTU 2 - QC PWTU2` |
| 20 | `Wave 1` | `C WAVE 1 - WAVE WAVE CONVENTIONAL` |
| 21 | `XRAY 1` | `XRAY 1 - XRAY XRAY` |

#### `UTAS WASH P1A-1 B6b`  —  20 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `PRE WASH 1 - WASH Pre-Wash 1` |
| 2 | `Assembly 2` | `PRE WASH 2 - WASH Pre-Wash 2` |
| 3 | `Assembly 3` | `PRE WASH 4 - WASH Pre-Wash 4` |
| 4 | `Assembly 4` | `PRE WASH 3 - WASH Pre-Wash 3` |
| 5 | `Link 1` | `WASH 1 - LINK WASH 1 LINK` |
| 6 | `Link 2` | `WASH 2 - LINK WASH 2 LINK` |
| 7 | `Link 3` | `WASH 3 - LINK WASH 3 LINK` |
| 8 | `Link 4` | `WASH 4 - LINK WASH 4 LINK` |
| 9 | `QC 1` | `INSP (WASH1) 1 - QC POST WASH 1 INSPECTION` |
| 10 | `QC 2` | `INSP (WASH2) 1 - QC POST WASH 2 INSPECTION` |
| 11 | `QC 3` | `INSP (WASH3) 1 - QC POST WASH 3 INSPECTION` |
| 12 | `QC 4` | `INSP (WASH4) 1 - QC Post Wash 4 Insp` |
| 13 | `Wash 1` | `WASH 1 - WASH Aqueous WASH 1` |
| 14 | `Wash 2` | `WASH (CHEM) 1 - WASH WASH` |
| 15 | `Wash 3` | `WASH 2 - WASH Aqueous WASH 2` |
| 16 | `Wash 4` | `WASH (CHEM) 2 - WASH WASH 2` |
| 17 | `Wash 5` | `WASH 3 - WASH Aqueous WASH 3` |
| 18 | `Wash 6` | `WASH (CHEM) 3 - WASH WASH 3` |
| 19 | `Wash 7` | `WASH 4 - WASH Aqueous WASH 4` |
| 20 | `Wash 8` | `WASH (CHEM) 4 - WASH WASH 4` |


### WABTEC

#### `WAB BE CC P1B-2`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `CC Cure 1` | `CUREB 1 - CURING BTM` |
| 2 | `CC Cure 2` | `CURET 1 - CURING TOP` |
| 3 | `CC Oven 1` | `BAKE 1 - BAKING PCBA` |
| 4 | `CC Oven 2` | `BAKE 2 - PCB Baking` |
| 5 | `CC QC 1` | `PRE COAT INSPB 1 - PRE COATING INSP BTM` |
| 6 | `CC QC 2` | `PRE COAT INSPT 1 - PRE COATING INSP TOP` |
| 7 | `CC QC 3` | `POST COAT INSPB 1 - POST COATING INSP BTM` |
| 8 | `CC QC 4` | `POST COAT INSPT 1 - POST COATING INSP TOP` |
| 9 | `CC Spray 1` | `ACOATB 1 - AUTO COATING BTM` |
| 10 | `CC Spray 2` | `ACOATT 1 - AUTO COATING TOP` |
| 11 | `De-Mask 1` | `DEMASKB 1 - UNMASKING BTM 1` |
| 12 | `De-Mask 2` | `DEMASKT 1 - UNMASKING TOP 1` |
| 13 | `Mask 1` | `MASKB 1 - MASKING BTM 1` |
| 14 | `Mask 2` | `MASKT 1 - MASKING TOP 1` |

#### `WAB BE ESS P1A-1`  —  1 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `ESS 1` | `ESS 1 - ESS` |

#### `WAB BE FVT P1B-2`  —  11 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `FVT 1` | `FVT (DOM) 1 - DOM DOWNLOADING` |
| 2 | `FVT 2` | `FVT 1 - FVT 1` |
| 3 | `FVT 3` | `FVT 1 - FVT 2` |
| 4 | `FVT 4` | `FVT 1 - FVT 3` |
| 5 | `FVT 5` | `FVT 1 - FVT 4` |
| 6 | `FVT 6` | `FVT 1 - FVT 5` |
| 7 | `FVT 7` | `FVT 1 - I2C Checking` |
| 8 | `Hi-Pot 1` | `HIPOT 1 - Hipot` |
| 9 | `Program 1` | `PROG 1 - PROGRAMMING` |
| 10 | `Program 2` | `PROG (QNX) 1 - QNX PROGRAMMING` |
| 11 | `Program 3` | `PROG (CLPD) 1 - CPLD Programming` |

#### `WAB BE P1B-2`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `FRONT MA 1 - FRONT MECH ASSY 1` |
| 2 | `Assembly 2` | `FRONT MA 1 - SMART TORQUE 1` |
| 3 | `QC 1` | `FRONT MA 1 - MAI 1` |
| 4 | `Solder 1` | `MSOLDER 1 - M.SOLDERING` |

#### `WAB HLA P1B-2`  —  17 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Assembly 1` | `BACK MA 1 - BACK MECH ASSY 1` |
| 2 | `Assembly 2` | `BACK MA 1 - SMART TORQUE 2` |
| 3 | `Assembly 3` | `BACK MA 2 - BACK MECH ASSY 2` |
| 4 | `Assembly 4` | `BACK MA 2 - SMART TORQUE 3` |
| 5 | `Assembly 5` | `BACK MA 3 - BACK MECH ASSY 3` |
| 6 | `Assembly 6` | `BACK MA 3 - SMART TORQUE 4` |
| 7 | `Assembly 7` | `BACK MA 4 - BACK MECH ASSY 4` |
| 8 | `Assembly 8` | `BACK MA 4 - SMART TORQUE 5` |
| 9 | `Bonding 1` | `BOND 1 - BONDING 1` |
| 10 | `FNI 1` | `FNI 1 - FNI 1 VIP` |
| 11 | `FNI 2` | `FNI  2 - FNI 2 VIP` |
| 12 | `Link 1` | `BACK MA 1 - MA LINK` |
| 13 | `OBA 1` | `OBA 1 - OQA 1 VIP` |
| 14 | `OBA 2` | `OBA 2 - OQA 2 VIP` |
| 15 | `Oven 1` | `BAKE 1 - BAKING PCBA` |
| 16 | `Packout 1` | `PACKOUT - PACKOUT` |
| 17 | `QC 1` | `PMI 1 - PMI` |

#### `WAB SMT P1A-1 B5a`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Dispense TOP 1` | `GLUET 1 - GLUET01` |
| 5 | `Label 1` | `BIRTH 1 - BIRTH` |
| 6 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 7 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 8 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 9 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 10 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 11 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 12 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 13 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 14 | `TSI 1` | `TSI 1 - TSI` |

#### `WAB SMT P1A-1 B6a`  —  14 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `AOI BOT 1` | `AOIB 1 - AOI BTM` |
| 2 | `AOI TOP 1` | `AOIT 1 - AOI TOP` |
| 3 | `BSI 1` | `BSI 1 - BSI` |
| 4 | `Dispense TOP 1` | `GLUET 1 - GLUET01` |
| 5 | `Label 1` | `BIRTH 1 - BIRTH` |
| 6 | `Placement BOT 1` | `SMTB 1 - SMTB01` |
| 7 | `Placement TOP 1` | `SMTT 1 - SMTT01` |
| 8 | `Reflow BOT 1` | `REFLOWB 1 - REFLOW SOLDERING BTM` |
| 9 | `Reflow TOP 1` | `REFLOWT 1 - REFLOW SOLDERING TOP` |
| 10 | `SCR BOT 1` | `SCRB 1 - SCRB01` |
| 11 | `SCR TOP 1` | `SCRT 1 - SCRT01` |
| 12 | `SPI BOT 1` | `SPIB 1 - SPI BTM` |
| 13 | `SPI TOP 1` | `SPIT 1 - SPI TOP` |
| 14 | `TSI 1` | `TSI 1 - TSI` |

#### `WAB TH AI P1A-1`  —  3 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Auto Insert 1` | `AI 1 - AUTO INSERT 1` |
| 2 | `QC 1` | `AI INSP 1 - AI Insp` |
| 3 | `QC 5` | `(no alias)` |

#### `WAB TH OVEN P1B-2`  —  4 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Oven 1` | `BAKE 1 - BAKING PCBA WASH 1` |
| 2 | `Oven 2` | `BAKE 2 - BAKING PCBA WASH 2` |
| 3 | `Oven 3` | `BAKE 3 - BAKING PCBA WASH 3` |
| 4 | `Oven 4` | `BAKE 4 - BAKING PCBA WASH 4` |

#### `WAB TH P1A-1 B5b`  —  16 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER 1 - Router` |
| 2 | `Dispense 1` | `CHEMASK 1 - PRE MI` |
| 3 | `ICT 1` | `ICT 1 - ICT` |
| 4 | `ICT 2` | `FPROBE 1 - Flying probe` |
| 5 | `Link 1` | `MIB 1 - MI BTM LINK` |
| 6 | `Link 2` | `MIT 1 - MI TOP LINK` |
| 7 | `Link 3` | `LINK AOP - AOP LINK` |
| 8 | `MI 1` | `MIB 1 - MI BTM 1` |
| 9 | `MI 2` | `MIT 1 - MI TOP 1` |
| 10 | `Press 1` | `PFIT 1 - Press Fit` |
| 11 | `THI 1` | `TSTH 1 - TSTH` |
| 12 | `Touch Up 1` | `PWTUB 1 - PWTU BTM` |
| 13 | `Touch Up 2` | `PWTUT 1 - PWTU TOP` |
| 14 | `Wave 1` | `CWAVEB 1 - CONVENTIONAL WAVE SOLDERING BTM` |
| 15 | `Wave 2` | `CWAVET 1 - CONVENTIONAL WAVE SOLDERING TOP` |
| 16 | `XRAY 1` | `XRAY 1 - XRAY` |

#### `WAB TH P1A-1 B6b`  —  10 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Depanel 1` | `ROUTER 1 - Router` |
| 2 | `Dispense 1` | `CHEMASK 1 - PRE MI` |
| 3 | `Link 1` | `MIB 1 - MI BTM LINK` |
| 4 | `Link 2` | `MIT 1 - MI TOP LINK` |
| 5 | `MI 1` | `MIB 1 - MI BTM 1` |
| 6 | `MI 2` | `MIT 1 - MI TOP 1` |
| 7 | `Touch Up 1` | `PWTUB 1 - PWTU BTM` |
| 8 | `Touch Up 2` | `PWTUT 1 - PWTU TOP` |
| 9 | `Wave 1` | `CWAVEB 1 - CONVENTIONAL WAVE SOLDERING BTM` |
| 10 | `Wave 2` | `CWAVET 1 - CONVENTIONAL WAVE SOLDERING TOP` |

#### `WAB TH WASH P1A-1 B6b`  —  13 steps

| # | Process | Alias |
|---:|---|---|
| 1 | `Link 1` | `PRE WASH 1 - WASH 1 LINK` |
| 2 | `Link 2` | `PRE WASH 2 - WASH 2 LINK` |
| 3 | `Link 3` | `PRE WASH 3 - WASH 3 LINK` |
| 4 | `Link 4` | `PRE WASH 4 - WASH 4 LINK` |
| 5 | `QC 1` | `POST WASH 1 - Post Wash 1 Insp` |
| 6 | `QC 2` | `POST WASH INSP 2 - Post Wash 2 Insp` |
| 7 | `QC 3` | `POST WASH INSP 3 - Post Wash 3 Insp` |
| 8 | `QC 4` | `POST WASH INSP 4 - Post Wash 4 Insp` |
| 9 | `Test 1` | `TEST (IONIC) 1 - IONIC TEST 1` |
| 10 | `Wash 1` | `WASH 1 - WASH 1` |
| 11 | `Wash 2` | `WASH 2 - WASH 2` |
| 12 | `Wash 3` | `WASH 3 - WASH 3` |
| 13 | `Wash 4` | `WASH 4 - WASH 4` |

