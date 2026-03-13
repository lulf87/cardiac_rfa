# Uncertainty-aware reduced 2D electro-thermal modeling of transmural lesion formation during radiofrequency cardiac ablation under uncertain contact and cooling conditions

Author names and affiliations to be added by the authors

Corresponding author: to be added

## Abstract

**Background:** Reduced-complexity computational models may enable interpretable comparison of radiofrequency (RF) ablation protocols under uncertain catheter–tissue contact and cooling conditions, but these models must report their assumptions and probability-estimation uncertainty transparently.

**Objective:** To develop and test a two-dimensional electro-thermal lesion model for comparative assessment of standard RF, high-power short-duration (HPSD), and very-high-power short-duration (vHPSD) protocols across wall thickness, contact surrogate, and cooling conditions.

**Methods:** A reduced electrode–blood–myocardium model was implemented using a quasi-static electrical solve, transient bioheat transfer, and Arrhenius thermal damage. Deterministic sweeps were performed over protocol, wall thickness, insertion depth as a contact surrogate, and effective convective cooling coefficient. Model outputs included lesion depth, maximum width, lesion area, depth fraction, depth-to-width ratio, peak temperature, transmurality, and an overheating proxy based on temperatures at or above 100 °C. Uncertainty propagation treated insertion depth and cooling as truncated-normal variables and used 64 samples per nominal cell; transmurality and overheating probabilities were reported with 95% Wilson-score confidence intervals.

**Results:** Across the deterministic sweeps, lesion penetration ranked standard RF > HPSD > vHPSD, and this ordering was mirrored by maximum width and lesion area. In the uncertainty-aware maps, standard RF occupied the broadest transmurality-success region, HPSD reached an intermediate regime concentrated in thin-wall settings, and vHPSD remained non-transmural across the scanned cells while showing the greatest overheating susceptibility under thin-wall, weak-cooling, high-contact conditions. Median half-widths of the Wilson-score intervals were 0.028 for transmurality probability and 0.028 for overheating probability, with maxima of 0.113 and 0.119, respectively. A literature-derived benchmark reproduced the protocol-level ranking reported experimentally but showed underestimation of absolute lesion depth under the nominal reduced-model setup.

**Conclusions:** The proposed reduced 2D framework provides a low-cost, interpretable approach for comparative lesion mapping and uncertainty-aware risk visualization. Under the present model assumptions, standard RF retained the highest transmural potential, HPSD occupied an intermediate regime, and vHPSD remained shallowest while showing the strongest overheating susceptibility. The framework is intended for methodology-focused comparative analysis rather than patient-specific lesion prediction.

**Keywords:** radiofrequency catheter ablation; electro-thermal modeling; uncertainty quantification; transmural lesion formation; HPSD; vHPSD

## 1. Introduction

Radiofrequency catheter ablation is widely used to create controlled thermal lesions in cardiac tissue, with the practical objective of achieving durable conduction block while avoiding collateral injury. Lesion formation depends on the interplay among protocol, tissue thickness, surface cooling, and catheter–tissue contact. These dependencies have motivated extensive computational work over the last three decades, spanning classical bioheat implementations, detailed multiphysics models, and recent protocol-comparison studies in high-power short-duration ablation [1–4].

Short-duration high-power strategies have intensified interest in protocol-specific trade-offs. Experimental comparisons have shown that shorter, higher-power applications can produce shallower lesions than longer conventional applications, even when the overall lesion footprint remains clinically useful [3]. In a temperature-controlled vHPSD setting, lesion size may also saturate with increasing contact force once contact reaches approximately 15 g, suggesting that increasingly aggressive contact does not necessarily yield proportionally deeper lesions [4]. These observations motivate computational frameworks that can map both efficacy-oriented quantities such as lesion penetration and risk-oriented quantities such as overheating susceptibility.

A practical difficulty is that high-fidelity three-dimensional or fully coupled models are computationally expensive and poorly suited to broad parameter sweeps on limited hardware. For an initial methodology-focused study, a reduced two-dimensional model offers a useful compromise: it preserves the dominant electro-thermal lesion-formation mechanisms while remaining inexpensive enough for deterministic sweeps and uncertainty propagation. Previous computational work has also shown that a dynamic contact model including heartbeat-induced electrode motion can be closely approximated by an equivalent average static insertion depth, supporting the use of a reduced contact surrogate in a first-pass comparative model [2].

The gap addressed here is therefore not the absence of another deterministic lesion simulator, but the lack of a compact and interpretable framework for protocol-level risk mapping under uncertain contact and cooling conditions. Electrophysiologists are often interested in questions such as the following: under what combinations of wall thickness, contact, and cooling is a protocol likely to become transmural, and under what combinations does the same protocol begin to incur non-negligible overheating risk? These questions are more naturally answered by probability maps and trade-off summaries than by single deterministic contours.

Accordingly, this study develops a reduced 2D electro-thermal model to compare a standard protocol (30 W/30 s), an HPSD protocol (50 W/10 s), and a vHPSD protocol (90 W/4 s). Deterministic sweeps are first used to characterize lesion-depth and lesion-geometry trends across wall thickness, insertion depth, and cooling strength. Uncertainty propagation over contact and cooling is then used to generate transmurality-probability maps, overheating-probability maps, and depth-fraction summaries. The central hypothesis is that standard RF will retain the highest transmural potential over the scanned conditions, HPSD will occupy an intermediate regime, and vHPSD will remain shallowest while showing the least favorable overheating trade-off under thin-wall, high-contact conditions.

## 2. Methods

### 2.1 Reduced two-dimensional electro-thermal lesion model
We considered a reduced two-dimensional cross-sectional model representing a vertically contacting ablation electrode, the adjacent blood pool at the tissue surface, the myocardial wall, and a lower thermal buffer (Figure 1). The aim of the model was not to reproduce catheter-specific irrigation or chamber-scale flow fields in full detail, but to provide a computationally inexpensive comparative framework for exploring how protocol choice, wall thickness, contact surrogate, and cooling intensity jointly influence lesion formation.

The electrical subproblem was modeled under a quasi-static approximation,
`div(sigma grad(phi)) = 0`,
with Joule heating defined as
`q_RF = sigma |grad(phi)|^2`.
The thermal problem was represented using a transient bioheat formulation,
`rho c dT/dt = div(k grad(T)) + q_RF - w_b rho_b c_b (T - T_b)`.
In the present reduced implementation, the perfusion term was set to zero so that blood/tissue heat exchange entered primarily through the surface cooling boundary condition. Thermal injury was quantified using an Arrhenius damage integral,
`Omega(t) = integral A exp(-Ea / (R T(tau))) dt`,
with lesion boundary defined by `Omega >= 1`.

### 2.2 Geometry and computational domain
The computational domain width was 18 mm. The physical myocardial wall thickness was varied between 2 and 6 mm depending on the study arm, and an additional 4 mm lower thermal buffer was included to reduce boundary contamination. The electrode footprint at the tissue surface was represented by a 2 mm-wide top boundary segment. Lesion depth was measured only within the physical myocardial wall; the thermal buffer was excluded from lesion metrics.

### 2.3 Boundary and initial conditions
For the electrical problem, the lower boundary was grounded, the electrode segment at the top surface was assigned a unit potential, and the remaining top surface and lateral boundaries were electrically insulated. For the thermal problem, the side boundaries and the lower boundary were treated as zero-flux boundaries. The top surface was subject to an effective convective cooling condition with nominal coefficient `h`, representing combined blood-pool and catheter-adjacent cooling in a reduced manner. The initial temperature was 37 °C throughout the domain.

### 2.4 Protocol implementation and contact surrogate
Three protocol classes were compared: standard RF (30 W / 30 s), HPSD (50 W / 10 s), and vHPSD (90 W / 4 s). Insertion depth was used as a contact surrogate rather than explicit mechanical force. In the reduced model, insertion depth influenced lesion formation through (i) a contact-dependent source-gain term applied to the regularized Joule source and (ii) a local reduction in the effective convective coefficient over the electrode footprint.

### 2.5 Material parameters and lesion metrics
Baseline material parameters were electrical conductivity `sigma = 0.6 S/m`, thermal conductivity `k = 0.55 W/m/K`, density `rho = 1050 kg/m^3`, and specific heat `c = 3600 J/kg/K`. The Arrhenius parameters were `A = 7.39 × 10^39 s^-1` and `E_a = 2.577 × 10^5 J/mol`. Reported outputs were lesion depth, maximum lesion width, lesion area, depth fraction (depth/wall thickness), depth-to-width ratio, peak temperature, transmurality, and an overheating proxy defined by temperatures at or above 100 °C or non-zero area above 100 °C.

### 2.6 Numerical implementation and verification
All simulations were implemented in Python using a finite-difference formulation on structured grids. The baseline production discretization used a 281 × 141 grid and time step `Delta t = 0.05 s`. Grid convergence was assessed using 201 × 101, 281 × 141, and 361 × 181 grids for the 4 mm baseline case. Time-step convergence was assessed using 0.1 s, 0.05 s, and 0.025 s. Relative errors in lesion depth and peak temperature were computed against the finest tested grid and smallest tested time step, respectively.

### 2.7 Deterministic sweeps
Deterministic parameter sweeps were performed across protocol, wall thickness, nominal cooling coefficient, and nominal insertion depth. Representative deterministic results were summarized using lesion depth, maximum lesion width, lesion area, peak temperature, depth fraction, and depth-to-width ratio.

### 2.8 Uncertainty quantification
Uncertainty-aware analyses treated insertion depth and the effective cooling coefficient as uncertain inputs. For each nominal cell in the wall-thickness × cooling × insertion × protocol grid, insertion depth and cooling coefficient were sampled independently using truncated normal distributions. Insertion depth was assigned a standard deviation of 0.20 mm and truncated to [0.25, 2.50] mm. Cooling coefficient was assigned a coefficient of variation of 0.15 and truncated to [300, 4000] W m^-2 K^-1. The paper-level maps were generated using 64 samples per nominal cell, and transmurality and overheating probabilities were accompanied by 95% Wilson-score confidence intervals. Solver and UQ settings are summarized in Table 2.

### 2.9 Literature-derived benchmark
Because no geometry-matched experimental calibration was available, external comparison was limited to a trend-level literature-derived benchmark. The benchmark used protocol-matched lesion-depth values reported for 30 W / 30 s, 50 W / 10 s, and 90 W / 4 s by Nakagawa et al. [3]. This comparison was interpreted as protocol-level trend benchmarking rather than strict validation because tissue geometry, catheter configuration, and thermal boundaries were not matched one-to-one.

**Table 1. Protocols compared**

| Protocol label | Power | Duration | Role in this study |
| --- | --- | --- | --- |
| Standard RF | 30 W | 30 s | Conventional deeper reference protocol |
| HPSD | 50 W | 10 s | Intermediate high-power short-duration protocol |
| vHPSD | 90 W | 4 s | Very-high-power short-duration protocol |

**Table 2. Solver settings and uncertainty assumptions**

| Item | Value |
| --- | --- |
| Deterministic baseline grid | 281 × 141 |
| Time step Delta t | 0.050 s |
| Wall thickness levels | 2.0, 3.0, 4.0, 5.0, 6.0 mm |
| Nominal cooling levels h | 800.0, 1500.0, 2500.0 W m^-2 K^-1 |
| Nominal insertion levels | 0.5, 1.0, 1.5, 2.0 mm |
| UQ samples per cell | 64 |
| Insertion distribution | Truncated normal, mean = nominal, sd = 0.20 mm |
| Insertion support | [0.25, 2.50] mm |
| Cooling distribution | Truncated normal, mean = nominal, CV = 0.15 |
| Cooling support | [300, 4000] W m^-2 K^-1 |
| Probability interval | 95% Wilson score interval |
| Overheat proxy threshold | Tmax >= 100 °C or non-zero area above 100 °C |

**Table 3. Protocol-level literature benchmark points**

| Source | Protocol | Reported lesion depth [mm] | Simulated lesion depth [mm] | Notes |
| --- | --- | --- | --- | --- |
| Nakagawa et al. 2021 [3] | Standard RF (30 W / 30 s) | 6.6 | 2.755 | Trend-level protocol match |
| Nakagawa et al. 2021 [3] | HPSD (50 W / 10 s) | 4.9 | 1.764 | Trend-level protocol match |
| Nakagawa et al. 2021 [3] | vHPSD (90 W / 4 s) | 3.6 | 1.302 | Trend-level protocol match |

## 3. Results

### 3.1 Representative electro-thermal fields
Figure 2 illustrates representative temperature and damage fields for a 4 mm wall, nominal cooling (`h = 1500 W m^-2 K^-1`), and nominal insertion depth (1.0 mm). Under this condition, lesion depth decreased from standard RF to HPSD and then to vHPSD. The lesion contour also became progressively more superficial from standard RF to vHPSD, while the high-temperature region remained concentrated near the tissue surface for vHPSD.

### 3.2 Deterministic protocol comparisons
Across the deterministic sweeps (Figure 3), lesion penetration ranked standard RF > HPSD > vHPSD. This ordering was observed not only for lesion depth, but also for maximum lesion width and lesion area across the wall-thickness sweep. Increasing wall thickness reduced lesion penetration for all three protocols, while increasing insertion depth raised peak temperature. Increasing cooling reduced depth fraction and only modestly altered depth-to-width ratio. These deterministic results indicate that the reduced model does not favor standard RF only through a depth-only metric, but predicts systematically different lesion geometries across protocols.

### 3.3 Numerical verification
Grid and time-step studies (Figure 4) showed that the selected production discretization provided stable deterministic metrics for the baseline case. Relative changes from the selected to the finest resolution remained small for both lesion depth and peak temperature, supporting the use of the 281 × 141 grid and `Delta t = 0.05 s` in the comparative and uncertainty-aware sweeps.

### 3.4 Uncertainty-aware transmurality and overheating maps
The uncertainty-aware maps (Figures 5 and 6) showed that standard RF occupied the largest transmurality-success region, HPSD occupied an intermediate region concentrated in thinner walls and stronger-contact settings, and vHPSD remained non-transmural across the scanned parameter space. Standard RF reached transmurality probabilities of 1.0 throughout much of the 2 mm wall regime and in several 3 mm cells under favorable contact/cooling conditions. HPSD also achieved high transmurality probabilities in thin-wall settings, reaching 1.0 in the 2 mm regime and 0.83 at 3 mm under weak cooling and nominal insertion. By contrast, vHPSD yielded no transmural cells in the present scan (maximum transmurality probability = 0.0).

Overheating risk followed the opposite pattern. Standard RF remained essentially free of overheating under the scanned conditions (maximum overheating probability 0.016), HPSD showed a limited overheating-prone region (maximum 0.516), and vHPSD showed the largest overheating susceptibility, reaching 1.0 under thin-wall, high-contact, weak-cooling conditions. The supplementary median depth-fraction maps (Figure S1) provided a continuous counterpart to the binary transmurality maps and preserved the same protocol ordering.

### 3.5 Confidence intervals on probability estimates
For the paper-level uncertainty maps, each nominal cell was evaluated using 64 samples. Wilson-score confidence intervals were computed for all transmurality and overheating probabilities. Supplementary Figure S3 summarizes the distribution of confidence-interval half-widths across all cells. The median half-width was 0.028 for transmurality probability and 0.028 for overheating probability, with maxima of 0.113 and 0.119, respectively. Compared with the earlier exploratory low-sample maps, the revised paper-level maps are materially less quantized and support a more defensible probabilistic interpretation.

### 3.6 Literature-derived benchmark
Figure 8 compares protocol-matched simulated lesion depth with literature-derived depth values. The reduced model reproduced the literature-reported ranking of standard RF > HPSD > vHPSD (Figure 8b), but the absolute simulated depths were consistently lower than the reported values (Figure 8a). Under the nominal reduced-model setup, the simulated depths were 2.755, 1.764, and 1.302 mm for standard RF, HPSD, and vHPSD, respectively, compared with reported values of 6.6, 4.9, and 3.6 mm. This pattern supports the present framework as a trend-level comparative and uncertainty-aware protocol-mapping tool rather than a geometry-matched predictive model.

## 4. Discussion

This study presents a reduced two-dimensional electro-thermal framework for comparing standard RF, HPSD, and vHPSD lesion formation under varying wall thickness, contact surrogate, and cooling conditions. The main contribution is not the deterministic depth ranking itself, which is unsurprising given the protocol definitions, but the uncertainty-aware comparative framework that maps transmurality success and overheating susceptibility across uncertain surface-contact and cooling conditions.

A first key finding is that the deterministic ranking remained stable across the explored settings: standard RF produced the deepest lesions, HPSD occupied an intermediate position, and vHPSD produced the shallowest lesions. Importantly, this ordering was mirrored not only in depth, but also in maximum lesion width and lesion area. The expanded geometry metrics therefore reduce the concern that the model unfairly favors standard RF by reporting depth alone.

A second key finding is that uncertainty-aware maps revealed a sharper trade-off than the deterministic comparisons alone. Under the present assumptions, standard RF occupied the broadest transmural-success region, HPSD reached transmurality in a narrower subset of thin-wall / stronger-contact settings, and vHPSD remained mostly non-transmural while showing the strongest overheating susceptibility in thin-wall, weak-cooling, high-contact conditions. These results should be interpreted as model-based comparative findings under the present reduced 2D assumptions, not as general clinical claims. In particular, the model does not include catheter-specific temperature-control logic, explicit irrigation-jet physics, or chamber-scale flow.

The study also highlights the importance of reporting uncertainty assumptions transparently. The earlier exploratory maps were useful for model development but produced visually quantized probabilities consistent with very low sample counts. In the revised workflow, the paper-level maps use larger per-cell sample counts and report Wilson-score confidence intervals, making the probability interpretation more defensible and directly addressing a central methodological concern in uncertainty-aware computational modeling.

The present work has several limitations. First, the model is two-dimensional and reduced-complexity rather than anatomy-matched. Second, the contact surrogate is insertion-depth-based and does not include explicit mechanics. Third, cooling is represented by an effective surface heat-transfer coefficient rather than explicit blood or irrigation-flow simulation. Fourth, the external benchmark remains trend-level and limited in size. Finally, the current overheating proxy is based on temperatures reaching or exceeding 100 °C and should not be interpreted as a mechanistic steam-pop or char model.

Despite these limitations, the framework is potentially useful as a low-cost comparative tool for protocol mapping. Future work should include catheter-specific temperature-control logic, explicit irrigation or chamber-flow surrogates, stronger geometry-matched validation, and broader protocol-matched literature benchmarking. In that role, the current reduced model can serve as an efficient screening or hypothesis-generation tool that complements, rather than replaces, higher-fidelity simulations and experiments.

## 5. Conclusion

A reduced two-dimensional electro-thermal model was developed to compare standard RF, HPSD, and vHPSD protocols under uncertain contact and cooling conditions. Across deterministic and probabilistic analyses, the model consistently ranked lesion penetration as standard RF > HPSD > vHPSD. Standard RF exhibited the broadest transmural-success region and the lowest overheating susceptibility, HPSD occupied an intermediate regime, and vHPSD remained shallowest while showing the strongest thermal-risk sensitivity under thin-wall, aggressive-contact conditions.

The revised uncertainty workflow, which included 64 samples per nominal cell and Wilson-score confidence intervals, strengthened the interpretability of the transmurality and overheating maps. The literature-derived benchmark reproduced the protocol-level ranking reported experimentally but underestimated absolute lesion depth, indicating that the present framework is most appropriate for comparative and uncertainty-aware protocol mapping rather than patient-specific quantitative lesion prediction.

## Data availability

Code, frozen figures, benchmark assets, and manuscript materials are organized within the accompanying project repository and submission package.

## Funding

To be added by the authors.

## Acknowledgements

To be added by the authors.

## Conflict of interest

The authors declare that the conflict-of-interest statement will be finalized prior to submission.

## References

1. González-Suárez A, Pérez JJ, Irastorza RM, D'Avila A, Berjano E. Computer modeling of radiofrequency cardiac ablation: 30 years of bioengineering research. Comput Methods Programs Biomed. 2022;214:106546. doi:10.1016/j.cmpb.2021.106546.
2. Pérez JJ, et al. Computer modeling of radiofrequency cardiac ablation including heartbeat-induced electrode displacement. Comput Biol Med. 2022;144:105346. doi:10.1016/j.compbiomed.2022.105346.
3. Nakagawa H, Ikeda A, Sharma T, Govari A, Ashton J, Maffre J, et al. Comparison of in vivo tissue temperature profile and lesion geometry for radiofrequency ablation with high power-short duration and moderate power-moderate duration: effects of thermal latency and contact force on lesion formation. Circ Arrhythm Electrophysiol. 2021;14(7):e009899. doi:10.1161/CIRCEP.121.009899.
4. Yamaguchi J, Takigawa M, Goya M, Martin CA, Negishi M, Yamamoto T, et al. Impact of contact force on the lesion characteristics of very high-power short-duration ablation using a QDOT-MICRO catheter. J Arrhythm. 2024;40:247-255. doi:10.1002/joa3.12992.
5. Pennes HH. Analysis of tissue and arterial blood temperatures in the resting human forearm. J Appl Physiol. 1948;1:93-122.
6. Henriques FC Jr. Studies of thermal injury V: the predictability and the significance of thermally induced rate processes leading to irreversible epidermal injury. Arch Pathol. 1947;43:489-502.
7. Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc. 1927;22(158):209-212.
8. Arrhenius S. On the reaction velocity of the inversion of cane sugar by acids. Z Phys Chem. 1889;4:226-248.

## Appendix A. Supplementary figures

Figure S1. Median depth-fraction maps under uncertain contact and cooling conditions. Rows correspond to standard RF, HPSD, and vHPSD; columns correspond to weak, nominal, and strong cooling.

Figure S2. Alternative trade-off summary using transmurality probability and overheating probability. Marker shape denotes protocol and marker color denotes wall thickness.

Figure S3. Distribution of 95% Wilson-score confidence-interval half-widths for (a) transmurality probability and (b) overheating probability across all nominal cells in the paper-level uncertainty maps.
