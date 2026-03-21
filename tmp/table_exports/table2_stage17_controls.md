| Item | exported_value | status | source_file | manuscript_value | matches_manuscript |
| --- | --- | --- | --- | --- | --- |
| Deterministic production grid | 281 x 141 | AUTO | simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml | 281 x 141 | YES |
| Time step | 0.05 s | AUTO | simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml | 0.05 s | YES |
| Wall thickness levels | 2.0, 3.0, 4.0, 5.0, 6.0 mm | AUTO | simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml | 2.0, 3.0, 4.0, 5.0, 6.0 mm | YES |
| Nominal cooling coefficients | 800, 1500, 2500 W m^-2 K^-1 | AUTO | simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml | 800, 1500, 2500 W m^-2 K^-1 | YES |
| Nominal insertion levels | 0.5, 1.0, 1.5, 2.0 mm | AUTO | simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml | 0.5, 1.0, 1.5, 2.0 mm | YES |
| Comparator set | 30 W / 30 s, 50 W / 10 s, 90 W / 4 s fixed, 90 W / 4 s temperature-limited | AUTO | simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml | 30 W / 30 s, 50 W / 10 s, 90 W / 4 s fixed, 90 W / 4 s temperature-limited | YES |
| Controller sensor | MANUAL | MANUAL | papers/V13/CMBBE_RF_ablation_reduced_model_main.docx :: Table 2; supporting config simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml | Surface-adjacent temperature surrogate | NO |
| Controller target / ceiling | 70 °C / 80 °C | AUTO | simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml | 70 °C / 80 °C | YES |
| Controller sample period | 0.05 s | AUTO | simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml | 0.05 s | YES |
| Post-pulse latency window | 8.0 s | AUTO | simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml | 8.0 s | YES |
| Phase-preparation grid size | 5 x 3 x 4 x 4 = 240 protocol-cell evaluations | AUTO | simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml; simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml | 5 x 3 x 4 x 4 = 240 protocol-cell evaluations | YES |
| Primary interpretive outputs | MANUAL | MANUAL | papers/V13/CMBBE_RF_ablation_reduced_model_main.docx :: Table 2 | Lesion depth, depth fraction, delivered energy, mean applied power, peak temperature | NO |
| Secondary internal proxies | MANUAL | MANUAL | papers/V13/CMBBE_RF_ablation_reduced_model_main.docx :: Table 2 | Lesion width, lesion area, overheat area (T ≥ 100 °C) | NO |
| Calibration status | MANUAL | MANUAL | papers/V13/CMBBE_RF_ablation_reduced_model_main.docx :: Table 2 | Contact/cooling surrogate coefficients retained from the preceding implementation; no formal re-estimation or identifiability analysis performed here | NO |
| Supplementary UQ status | MANUAL | MANUAL | papers/V13/CMBBE_RF_ablation_reduced_model_main.docx :: Table 2 | Reference uncertainty figures from the fixed-power three-protocol formulation are provided for completeness only and are not the primary evidentiary basis for the comparator-aware conclusions | NO |