# 《修订后论文正文》

## Title page

Uncertainty-aware reduced 2D electro-thermal modeling of transmural lesion formation during radiofrequency cardiac ablation


**[待作者补充作者与单位信息]**


**[待作者补充通讯作者信息]**


## Abstract

Background: Reduced-complexity electro-thermal models may offer a practical route to comparative radiofrequency (RF) ablation analysis on modest hardware, provided that assumptions, uncertainty inputs, and probability-estimation uncertainty are reported transparently.

Objective: To develop a reduced two-dimensional uncertainty-aware model for comparing standard RF, high-power short-duration (HPSD), and very-high-power short-duration (vHPSD) lesion formation across wall thickness, contact surrogate, and surface-cooling conditions.

Methods: A vertically contacting electrode-blood-myocardium model was implemented using a quasi-static electrical solve, transient bioheat transfer, and Arrhenius thermal damage. Deterministic sweeps were performed over wall thickness, nominal cooling coefficient, insertion depth as a contact surrogate, and three protocol classes (30 W/30 s, 50 W/10 s, and 90 W/4 s). The regularized unit-potential Joule source was scaled to the applied power and modulated by insertion depth through explicit source-gain and local cooling-reduction rules. Reported outputs included lesion depth, maximum width, lesion area, depth fraction, depth-to-width ratio, peak temperature, transmurality, and an overheating proxy based on temperatures >= 100 C. Uncertainty propagation treated insertion depth and cooling coefficient as truncated-normal inputs and used 64 stratified samples per nominal cell; transmurality and overheating probabilities were reported with 95% Wilson-score confidence intervals.

Results: Deterministically, lesion penetration and lesion extent ranked standard RF > HPSD > vHPSD. Under the baseline nominal condition, lesion depth/width/area were 2.76 mm/3.82 mm/8.66 mm^2 for standard RF, 1.76 mm/3.15 mm/4.47 mm^2 for HPSD, and 1.30 mm/2.69 mm/2.63 mm^2 for vHPSD. In the uncertainty-aware maps, standard RF occupied the broadest transmurality-success region, HPSD reached a narrower thin-wall / higher-contact regime, and vHPSD remained predominantly non-transmural while showing the greatest overheating susceptibility in thin-wall, weak-cooling, high-contact conditions. Median 95% Wilson half-widths were 0.028 for transmurality probability and 0.028 for overheating probability. A literature-derived benchmark reproduced the protocol-level depth ranking reported experimentally but underestimated absolute lesion depth under the nominal reduced-model setup.

Conclusions: The proposed reduced 2D framework provides an interpretable and low-cost method for comparative lesion mapping and uncertainty-aware risk visualization. Under the present assumptions, standard RF retained the highest transmural potential, HPSD occupied an intermediate regime, and vHPSD remained shallowest while most susceptible to overheating. The framework is intended for comparative methodology-focused analysis rather than patient-specific lesion prediction.

Keywords: radiofrequency catheter ablation; electro-thermal modeling; uncertainty quantification; transmural lesion formation; HPSD; vHPSD

## 1. Introduction

Radiofrequency catheter ablation remains a standard thermal strategy for creating irreversible myocardial injury in the treatment of cardiac arrhythmias. Lesion size and shape are governed by the interplay among delivered power, application duration, catheter-tissue contact, local cooling, and tissue thickness **[1-3]**. Classical bioheat and thermal-injury models have long been used to study these mechanisms **[4-8]**, while contemporary cardiac-ablation reviews show that computational modeling now spans simplified two-dimensional studies, irrigated-electrode models, dynamic contact models, and broader multiphysics frameworks **[1-3,9]**.

High-power short-duration strategies have drawn particular interest because they alter the balance between resistive and conductive heating **[10-20]**. Experimental and clinical studies indicate that HPSD can shorten RF delivery time while maintaining lesion efficacy in selected contexts **[17-20]**. At the same time, lesion geometry is protocol dependent: computer and experimental studies have shown that increasing power while shortening duration does not simply scale lesion depth proportionally, and vHPSD lesions may remain relatively shallow in thick myocardium **[10,13-16,21-22]**. In temperature-controlled 90 W/4 s ablation, lesion size also appears to saturate once contact force exceeds approximately 15 g **[21]**.

For methodology development on modest hardware, however, full three-dimensional or catheter-specific models are often too expensive for broad parameter sweeps. Reduced models remain useful if they are explicit about what they can and cannot represent. Earlier work has shown, for example, that simplified models may predict lesion depth and maximum tissue temperature reasonably well while failing to reproduce blood temperature and surface-width behavior in irrigated-tip settings **[3]**. Likewise, a dynamic-contact RFCA model showed that under selected moderate-contact conditions, heartbeat-induced displacement could be approximated by an average static insertion depth for lesion-depth prediction **[9]**. These observations support the present strategy: a reduced two-dimensional framework oriented toward comparative lesion mapping rather than patient-specific lesion prediction.

The specific gap addressed here is not the absence of another deterministic lesion simulator, but the lack of an inexpensive uncertainty-aware framework for protocol-level risk mapping under uncertain contact and cooling conditions. Electrophysiologists are often interested in questions such as: under what combinations of wall thickness, contact, and cooling is a protocol likely to become transmural, and where does the same protocol begin to incur appreciable overheating risk? These questions are more naturally answered by probability maps and trade-off summaries than by isolated deterministic contours.

Accordingly, this study develops a reduced 2D electro-thermal model to compare a conventional protocol (30 W/30 s), an HPSD protocol (50 W/10 s), and a vHPSD protocol (90 W/4 s). Deterministic sweeps are first used to characterize lesion depth, width, area, and temperature trends across wall thickness, insertion depth, and cooling. Uncertainty propagation over contact surrogate and cooling then generates transmurality-probability maps, overheating-probability maps, and depth-fraction summaries. The central hypothesis is that standard RF will occupy the broadest transmural-success region, HPSD will show an intermediate thin-wall regime, and vHPSD will remain shallower while showing greater overheating susceptibility under thin-wall, high-contact conditions.

## 2. Methods

### 2.1 Reduced two-dimensional electro-thermal lesion model

We considered a reduced two-dimensional cross-sectional model composed of a vertically contacting electrode footprint, the adjacent blood-pool boundary, a myocardial wall, and a lower thermal buffer. The objective was comparative lesion analysis rather than catheter-specific reproduction of irrigation jets, chamber-scale flow, or feedback-controlled temperature regulation. **Figure 1 summarizes the reduced geometry and computational workflow.**

The electrical subproblem was solved in quasi-static form:

∇·(σ∇ϕ) = 0

where ϕ is electric potential and σ is electrical conductivity. A unit-potential solution was first obtained, and the corresponding unit Joule source was computed as:

q_unit = σ|∇ϕ|^2

The thermal problem was represented using a transient bioheat formulation:

ρc ∂T/∂t = ∇·(k∇T) + q_RF − ω_bρ_bc_b(T − T_b)

where T is temperature, ρ density, c specific heat, and k thermal conductivity. In the present implementation, the perfusion term was set to zero, so that blood-mediated cooling entered primarily through the surface boundary condition. Thermal injury was quantified using the Arrhenius damage integral:

Ω(t) = ∫_0^t A exp[−E_a/(RT(τ))] dτ

and lesion boundary was defined by **[4-8]**.

### 2.2 Geometry and computational domain

The domain width was 18 mm. Physical myocardial wall thickness was varied from 2 to 6 mm. An additional 4 mm lower thermal buffer was included to reduce boundary contamination, but this buffer was excluded from lesion metrics. The electrode footprint at the tissue surface was represented by a 2-mm-wide top boundary segment. The baseline production grid for the 4-mm wall case used 281 x 141 nodes, with the number of depth nodes rescaled proportionally for other wall-thickness settings.

### 2.3 Boundary and initial conditions

The lower boundary of the electrical domain was grounded, the electrode segment at the top surface was assigned a unit potential, and the remaining top-surface and lateral boundaries were electrically insulated. For the thermal problem, the lateral and lower boundaries were zero-flux. The top surface was subject to an effective convective condition with nominal coefficient h_nom, representing combined blood-pool and catheter-adjacent cooling in reduced form. The initial temperature was 37 C throughout the domain.

### 2.4 Power scaling and contact surrogate implementation

Three protocol classes were compared: standard RF (30 W/30 s), HPSD (50 W/10 s), and vHPSD (90 W/4 s). Contact was represented using insertion depth d_ins rather than explicit force. In the model implementation, the unit Joule source was first smoothed with a Gaussian kernel and shifted in depth according to:

Δy = α_shift d_ins

**The protocol definitions used throughout the study are summarized in Table 1.**

where α_shift is the depth-shift coefficient. The regularized source q_reg was then scaled to the applied power according to:

q_RF = κ_P P S_c(d_ins) q_reg / ∫ q_reg dA

where P is the protocol power, κ_P = 6.8 W m^-1 per applied watt is the calibrated source-amplitude coefficient, and the contact-gain factor is:

S_c(d_ins) = max(0.5, 1 + β_P(d_ins − d_ref))

with d_ref = 1.0 mm and β_P = 0.16 mm^-1. Thus, larger insertion depths increase the effective source strength while preserving the regularized spatial pattern.

Contact also modified local cooling over the electrode footprint. On the footprint, the effective convective coefficient was:

h_foot = h_nom S_h(d_ins)

with

S_h(d_ins) = clip(1 − β_h(d_ins − d_ref), h_min, h_max)

where β_h = 0.35 mm^-1, h_min = 0.50, and h_max = 1.40. Outside the electrode footprint, the surface coefficient remained equal to h_nom. This construction allowed the contact surrogate to affect both local source intensity and local cooling in a transparent reduced-order manner.

### 2.5 Material parameters and lesion metrics

Baseline material parameters were σ = 0.6 S/m, k = 0.55 W m^-1 K^-1, ρ = 1050 kg m^-3, and c = 3600 J kg^-1 K^-1. The Arrhenius parameters were A = 7.39 × 10^39 s^-1 and E_a = 2.577 × 10^5 J mol^-1. Reported outputs were lesion depth, maximum lesion width, lesion area, depth fraction (depth/wall thickness), depth-to-width ratio, transmurality, peak temperature, and the area exposed to temperatures >= 100 C.

### 2.6 Numerical implementation and verification

The model was implemented in Python using a finite-difference discretization on structured grids. The unit-potential electrical problem and the implicit heat step were solved at each case using sparse linear algebra. Grid convergence was assessed using 201 x 101, 281 x 141, and 361 x 181 grids for the 4-mm baseline case. Time-step convergence was assessed using 0.10 s, 0.05 s, and 0.025 s. The selected production settings were 281 x 141 and Δt = 0.05 s. **The production solver, contact-surrogate, and uncertainty settings are summarized in Table 2.**

### 2.7 Deterministic sweeps

Deterministic sweeps were performed across protocol, wall thickness, nominal cooling coefficient, and nominal insertion depth. Wall thickness values were 2, 3, 4, 5, and 6 mm. Nominal cooling coefficients were 800, 1500, and 2500 W m^-2 K^-1. Nominal insertion depths were 0.5, 1.0, 1.5, and 2.0 mm. These sweeps were summarized using lesion depth, maximum width, lesion area, peak temperature, depth fraction, and depth-to-width ratio.

### 2.8 Uncertainty quantification

Insertion depth and cooling coefficient were treated as uncertain inputs. For each nominal wall-thickness x cooling x insertion x protocol cell, insertion depth and cooling coefficient were sampled independently using truncated normal distributions. Insertion depth was assigned a standard deviation of 0.20 mm and truncated to [0.25, 2.50] mm. Cooling coefficient was assigned a coefficient of variation of 0.15 and truncated to [300, 4000] W m^-2 K^-1. Each marginal distribution was sampled with 64 stratified draws per cell using an 8 x 8 stratified design with independent within-stratum randomization, after which the two variables were paired by randomized permutation. Transmurality and overheating probabilities were reported together with 95% Wilson-score confidence intervals **[7,23]**. **Supplementary Figure S3** summarizes the resulting confidence-interval half-width distributions.

### 2.9 Literature-derived benchmark

Because no geometry-matched experimental dataset was available, external comparison was limited to a protocol-level literature-derived benchmark. The benchmark was used to assess whether the reduced model reproduced the experimentally reported ranking of lesion depth across standard RF, HPSD, and vHPSD protocols **[10,14]**. This comparison is therefore interpreted as trend-level benchmarking rather than strict validation.

**Table 1.** Protocol definitions used throughout the deterministic and uncertainty-aware analyses.

| Protocol | Power (W) | Duration (s) | Nominal energy (J) | Role in comparison |
|---|---:|---:|---:|---|
| Standard RF | 30 | 30 | 900 | Conventional long-duration comparator |
| HPSD | 50 | 10 | 500 | Intermediate high-power short-duration comparator |
| vHPSD | 90 | 4 | 360 | Very-high-power short-duration comparator |

**Table 2.** Solver, contact-surrogate, and uncertainty settings used for the production analyses.

| Item | Value |
|---|---|
| Deterministic production grid | 281 x 141 |
| Time step | 0.05 s |
| Wall thickness levels | 2.0, 3.0, 4.0, 5.0, 6.0 mm |
| Nominal cooling coefficients | 800, 1500, 2500 W m^-2 K^-1 |
| Nominal insertion levels | 0.5, 1.0, 1.5, 2.0 mm |
| UQ samples per nominal cell | 64 |
| Insertion-depth distribution | truncated normal, SD 0.20 mm, support [0.25, 2.50] mm |
| Cooling-coefficient distribution | truncated normal, CV 0.15, support [300, 4000] W m^-2 K^-1 |
| Probability intervals | 95% Wilson score |
| Overheating proxy threshold | T >= 100 C |
| Contact power gain coefficient | 0.16 mm^-1 |
| Contact cooling-reduction coefficient | 0.35 mm^-1 |

## 3. Results

### 3.1 Deterministic protocol comparisons

Under the nominal baseline condition (4-mm wall thickness, insertion depth 1.0 mm, cooling coefficient 1500 W m^-2 K^-1), lesion extent ranked standard RF > HPSD > vHPSD across depth, width, and area. The baseline depth/width/area values were 2.76 mm/3.82 mm/8.66 mm^2 for standard RF, 1.76 mm/3.15 mm/4.47 mm^2 for HPSD, and 1.30 mm/2.69 mm/2.63 mm^2 for vHPSD. Peak temperature showed the opposite ordering, with vHPSD generating the hottest local response. Thus, the deterministic comparisons did not simply identify a depth ranking, but a broader lesion-geometry ordering across protocols. **Representative baseline temperature and damage fields are shown in Figure 2, and the corresponding deterministic trend summary across protocols is provided in Figure 3.**

### 3.2 Effects of wall thickness, insertion depth, and cooling

Increasing wall thickness reduced depth fraction across all protocols. Standard RF approached or reached transmurality in the 2-3 mm regime, whereas HPSD reached this regime only under a smaller subset of thin-wall / stronger-contact settings and vHPSD remained predominantly subtransmural across the scanned parameter space. Increasing insertion depth increased lesion depth, width, area, depth-to-width ratio, and peak temperature for all protocols. Increasing nominal cooling reduced lesion extent and peak temperature. These trends were consistent across multiple geometry metrics and therefore do not depend on depth alone.

### 3.3 Numerical verification

Grid- and time-step-refinement studies showed that the selected production settings were stable for the baseline case. Relative changes in lesion depth and peak temperature were small between the selected and finer settings, supporting the use of the selected grid and time step for the deterministic and uncertainty-aware sweeps. **These verification results are summarized in Figure 4.**

### 3.4 Uncertainty-aware transmurality and overheating maps

The uncertainty-aware maps showed that standard RF occupied the broadest transmurality-success region. HPSD occupied an intermediate region concentrated in thin-wall settings with greater nominal insertion depth. vHPSD remained predominantly non-transmural across the scanned cells. In contrast, overheating probability was concentrated mainly in vHPSD, especially under thin-wall, weak-cooling, high-contact conditions, while standard RF remained negligible in the current reduced model. Thus, the probability maps exposed a trade-off between deeper penetration and thermal-risk susceptibility that was not fully apparent from deterministic depth alone. **The transmurality-probability maps are shown in Figure 5, the corresponding overheating-probability maps in Figure 6, and the depth-risk trade-off summary in Figure 7. Median depth-fraction maps and an alternative probability-probability trade-off view are provided in Supplementary Figure S1 and Supplementary Figure S2, respectively.**

### 3.5 Confidence intervals on probability estimates

For the production uncertainty maps, each nominal cell was evaluated with 64 stratified samples. Wilson-score confidence intervals were computed for all transmurality and overheating probabilities. **Supplementary Figure S3** shows that most cells had relatively narrow confidence-interval half-widths, while a smaller set of near-transition cells retained larger uncertainty bounds. The median 95% Wilson half-widths were 0.028 for transmurality probability and 0.028 for overheating probability, with maxima of 0.113 and 0.119, respectively.

### 3.6 Literature-derived benchmark

The protocol-level literature benchmark reproduced the experimentally reported ranking in lesion depth: standard RF deepest, HPSD intermediate, and vHPSD shallowest. **The underlying protocol-matched benchmark points are listed in Table 3, and Figure 8 summarizes both point-wise depth agreement and protocol-level mean-depth trends.** However, the reduced model underestimated the absolute lesion depth values relative to the literature points under the nominal reduced-model setup. Accordingly, the benchmark supports the present framework as a trend-level comparative model rather than a geometry-matched predictive model.

Figure 1. Reduced 2D model geometry and workflow. Panel (a) shows the electrode footprint, blood-pool boundary, myocardium, and lower thermal buffer, together with the electrical and thermal boundary conditions. Panel (b) summarizes the computational workflow from unit-potential solve to power-scaled heat source, transient bioheat solution, Arrhenius damage, and lesion metrics.

Figure 2. Representative spatial fields for the three protocol classes under the baseline nominal case. The top row shows temperature fields and lesion-boundary contours; the bottom row shows thermal-damage fields expressed as log10(Omega).

Figure 3. Deterministic summary plots across the protocol comparison. Panels show lesion depth vs wall thickness, maximum width vs wall thickness, lesion area vs wall thickness, peak temperature vs insertion depth, depth fraction vs cooling coefficient, and depth-to-width ratio vs cooling coefficient. Standard RF, HPSD, and vHPSD are distinguished by both color and marker shape.

Figure 4. Grid and time-step verification for the baseline nominal case. The selected production grid and time step are indicated directly on the plots.

Figure 5. Transmurality-probability maps under uncertain contact and cooling conditions. Rows correspond to standard RF, HPSD, and vHPSD; columns correspond to the nominal cooling coefficients. Values are estimated from an 8 x 8 stratified design (64 samples) per nominal cell and only transition-region cells are numerically annotated.

Figure 6. Overheating-probability maps under uncertain contact and cooling conditions. The standard-protocol row is not shown because all scanned cells had overheating probability equal to zero under the current reduced-model assumptions. Values are estimated from an 8 x 8 stratified design (64 samples) per nominal cell.

Figure 7. Trade-off summary using median depth fraction and overheating probability. Marker shape denotes protocol, marker color denotes wall thickness, and the shaded region indicates a qualitatively favorable high-penetration / low-overheating region.

**Table 3.** Literature-derived protocol-level benchmark points used in Figure 8.

| Source / matched point | Protocol | Reported depth (mm) | Simulated depth (mm) | Reported width (mm) | Simulated width (mm) |
|---|---|---:|---:|---:|---:|
| Nakagawa2021 | Standard RF | 6.6 | 2.76 | 10.7 | 3.82 |
| Nakagawa2021 | HPSD | 4.9 | 1.76 | 9.2 | 3.15 |
| Nakagawa2021 | vHPSD | 3.6 | 1.30 | 8.2 | 2.69 |

**Figure 8.** Literature-derived benchmark of lesion-depth trends. **Panel (a) compares reported lesion depth and simulated lesion depth for the protocol-matched benchmark points using an identity line for visual reference. Panel (b) compares protocol-level mean reported and simulated lesion depth. The benchmark reproduced the protocol-level ranking but underestimated absolute depth.**

## 4. Discussion

This study presents a reduced two-dimensional electro-thermal framework for comparing standard RF, HPSD, and vHPSD lesion formation across wall thickness, contact surrogate, and cooling conditions. The main contribution is not the deterministic depth ranking itself—which is unsurprising given the protocol definitions—but the uncertainty-aware framework that maps comparative transmurality success and overheating susceptibility across uncertain contact and cooling settings.

A first key finding is that the deterministic ordering remained stable across multiple geometry metrics: standard RF produced the deepest, widest, and largest-area lesions; HPSD occupied an intermediate position; and vHPSD remained shallowest. The addition of width, area, and depth-to-width ratio directly addresses the concern that the model might otherwise privilege standard RF through depth-only reporting. Under the present nominal settings, the geometric ranking remained consistent across all three metrics.

A second key finding is that uncertainty-aware maps exposed a sharper trade-off than deterministic summaries alone. Standard RF occupied the broadest transmural-success region, HPSD reached transmurality only in a narrower thin-wall / higher-contact regime, and vHPSD remained mostly non-transmural while showing the highest overheating susceptibility under thin-wall, weak-cooling, high-contact conditions. These findings should be interpreted as comparative model outputs under the present reduced assumptions, not as general clinical claims. In particular, the model does not reproduce catheter-specific temperature-control logic, explicit irrigation-jet flow, or chamber-scale hemodynamics **[2-3,10,14-18,21]**.

The revised uncertainty workflow materially improved probability transparency. Earlier exploratory maps used low sample counts and produced strongly quantized probability patterns. In the present manuscript, the production maps are based on 64 stratified samples per nominal cell, and probability uncertainty is reported through Wilson-score confidence intervals. **Supplementary Figure S3** confirms that most cells have modest interval half-widths, while cells near transition regimes still retain broader uncertainty bounds. This makes the probability maps more defensible as comparative risk summaries.

The literature-derived benchmark should also be interpreted cautiously. The current comparison is protocol-matched rather than geometry-matched and therefore should not be described as strict validation. The reduced model reproduced the protocol-level ranking but underestimated absolute lesion depth under the nominal reduced-model setup. This underprediction is consistent with the simplified nature of the model, which omits explicit irrigation physics, catheter-specific temperature control, and richer chamber-scale flow **[2-3]**.

The present study has several limitations. First, the model is two-dimensional and reduced-complexity rather than anatomy-matched. Second, the contact surrogate is insertion-depth-based and does not include explicit mechanics, even though contact area and lesion size are known to be closely linked **[24]**. Third, cooling is represented by an effective surface heat-transfer coefficient rather than explicit blood or irrigation flow **[2-3]**. Fourth, the external benchmark remains limited in size. Finally, the overheating proxy is based on temperatures reaching or exceeding 100 C and should not be interpreted as a mechanistic steam-pop or char model **[8]**.

Despite these limitations, the framework remains useful as a low-cost comparative tool for protocol mapping on limited hardware. Future work should include catheter-specific temperature-control logic, richer cooling surrogates or explicit local flow, broader protocol-matched benchmarking, and stronger geometry-matched validation. In that role, the present model can serve as an efficient screening tool that complements rather than replaces higher-fidelity simulations and experiments.

## 5. Conclusion

A reduced two-dimensional electro-thermal model was developed to compare standard RF, HPSD, and vHPSD protocols under uncertain contact and cooling conditions. Across deterministic and uncertainty-aware analyses, lesion penetration ranked standard RF > HPSD > vHPSD, while overheating susceptibility was concentrated primarily in vHPSD. The revised uncertainty workflow, based on 64 stratified samples per nominal cell and Wilson-score confidence intervals, strengthened the interpretability of the resulting risk maps. The literature-derived benchmark reproduced the protocol-level depth ranking but underestimated absolute lesion depth, indicating that the present framework is most appropriate for comparative and uncertainty-aware protocol mapping rather than patient-specific quantitative lesion prediction.

## Data availability

Code, frozen figures, benchmark assets, and manuscript materials are organized in the accompanying project repository and paper package.

## Funding

**[待作者补充 Funding statement]**

## Acknowledgements

**[待作者补充 Acknowledgements]**

## Conflict of interest

The authors declare no scientific conflicts related to this methodology-focused computational study. Administrative declarations will be finalized before submission.

## References

**1. González-Suárez A, et al. Computer modeling of radiofrequency cardiac ablation: 30 years of bioengineering research. Comput Methods Programs Biomed. 2022;214:106546. doi:10.1016/j.cmpb.2021.106546.**

**2. González-Suárez A, et al. Computational modeling of open-irrigated electrodes for radiofrequency cardiac ablation including blood motion-saline flow interaction. PLoS One. 2016;11:e0150356. doi:10.1371/journal.pone.0150356.**

**3. González-Suárez A, et al. Should fluid dynamics be included in computer models of RF cardiac ablation by irrigated-tip electrodes? Biomed Eng Online. 2018;17:43. doi:10.1186/s12938-018-0471-4.**

**4. Pennes HH. Analysis of tissue and arterial blood temperatures in the resting human forearm. J Appl Physiol. 1948;1:93-122. doi:10.1152/jappl.1948.1.2.93.**

**5. Henriques FC Jr. Studies of thermal injury V. The predictability and significance of thermally induced rate processes leading to irreversible epidermal injury. Arch Pathol. 1947;43:489-502.**

**6. Arrhenius S. On the reaction velocity of the inversion of cane sugar by acids. Z Phys Chem. 1889;4:226-248.**

**7. Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc. 1927;22:209-212. doi:10.1080/01621459.1927.10502953.**

**8. Chang IA. Considerations for thermal injury analysis for RF ablation devices. Open Biomed Eng J. 2010;4:3-12. doi:10.2174/1874120701004010003.**

**9. Pérez JJ, et al. Computer modeling of radiofrequency cardiac ablation including heartbeat-induced electrode displacement. Comput Biol Med. 2022;144:105346. doi:10.1016/j.compbiomed.2022.105346.**

**10. Nakagawa H, et al. Comparison of in vivo tissue temperature profile and lesion geometry for radiofrequency ablation with high power-short duration and moderate power-moderate duration: effects of thermal latency and contact force on lesion formation. Circ Arrhythm Electrophysiol. 2021;14:e009899. doi:10.1161/CIRCEP.121.009899.**

**11. Kotadia ID, et al. High-power, short-duration radiofrequency ablation for the treatment of AF. Arrhythm Electrophysiol Rev. 2019;8:265-272. doi:10.15420/aer.2019.09.**

**12. Petras A, et al. Systematic characterization of high-power short-duration ablation: insight from an advanced virtual model. Europace. 2021;23:1587-1596. doi:10.1093/europace/euab103.**

**13. Irastorza RM, et al. Thermal latency adds to lesion depth after application of high-power short-duration radiofrequency energy: results of a computer-modeling study. J Cardiovasc Electrophysiol. 2018;29:322-327. doi:10.1111/jce.13363.**

**14. Reddy VY, et al. Pulmonary vein isolation with very high power, short duration, temperature-controlled lesions: the QDOT-FAST trial. JACC Clin Electrophysiol. 2019;5:778-786. doi:10.1016/j.jacep.2019.04.009.**

**15. Rozen G, et al. Safety and efficacy of delivering high-power short-duration radiofrequency ablation lesions utilizing a novel temperature sensing technology. Europace. 2018;20:f444-f450. doi:10.1093/europace/euy031.**

**16. Barkagan M, et al. High-power and short-duration ablation for pulmonary vein isolation: safety, efficacy, and long-term durability. J Cardiovasc Electrophysiol. 2018;29:1287-1296. doi:10.1111/jce.13651.**

**17. Chieng D, et al. Higher power short duration vs. lower power longer duration posterior wall ablation for atrial fibrillation and oesophageal injury outcomes: a prospective multi-centre randomized controlled study (Hi-Lo HEAT trial). Europace. 2023;25:417-425. doi:10.1093/europace/euac194.**

**18. Jin S, et al. High-power, short-duration ablation under the guidance of relatively low ablation index values for paroxysmal atrial fibrillation: long-term outcomes and characteristics of recurrent atrial arrhythmias. J Clin Med. 2023;12:971. doi:10.3390/jcm12030971.**

**19. Liu X, et al. Safety and efficacy of high power shorter duration ablation guided by ablation index or lesion size index in atrial fibrillation ablation: a systematic review and meta-analysis. J Interv Card Electrophysiol. 2021;62:535-545. doi:10.1007/s10840-021-00923-7.**

**20. Amin AM, et al. Efficacy and safety of high-power short-duration ablation for atrial fibrillation: a systematic review and meta-analysis of randomized controlled trials. J Interv Card Electrophysiol. 2024. doi:10.1007/s10840-024-01782-2.**

**21. Yamaguchi J, et al. Impact of contact force on the lesion characteristics of very high-power short-duration ablation using a QDOT-MICRO catheter. J Arrhythm. 2024;40:247-255. doi:10.1002/joa3.12992.**

**22. Iwakawa H, et al. Lesion depth optimization in high-power radiofrequency ablation: evaluating single high-power and combined very high-power applications. J Cardiovasc Electrophysiol. 2025;36:3212-3223. doi:10.1111/jce.16643.**

**23. Fahrenholtz SJ, et al. Generalized polynomial chaos based uncertainty quantification for planning MRgLITT procedures. Int J Hyperthermia. 2014;30:54-63.**

**24. Masnok K, et al. Catheter contact area strongly correlates with lesion area in radiofrequency cardiac ablation. Sci Rep. 2021;11:17009. doi:10.1038/s41598-021-96455-1.**

## Appendix A. Supplementary figures

**Supplementary Figure S1.** Median depth-fraction maps under uncertain contact and cooling conditions. Rows correspond to standard RF, HPSD, and vHPSD; columns correspond to the nominal cooling coefficients.

**Supplementary Figure S2.** Alternative trade-off summary using transmurality probability and overheating probability. This complementary view is provided to show the same uncertainty-aware trade-off in probability-probability space.

**Supplementary Figure S3.** Distribution of 95% Wilson-score confidence-interval half-widths for (a) transmurality probability and (b) overheating probability across all nominal cells in the production uncertainty maps.


# 《旧编号 → 新编号映射表》

| 旧编号 | 新编号 |
|---:|---:|

| 1 | 4 |

| 2 | 5 |

| 3 | 6 |

| 4 | 7 |

| 5 | 1 |

| 6 | 9 |

| 7 | 2 |

| 8 | 3 |

| 9 | 10 |

| 10 | 21 |

| 11 | 22 |

| 12 | 11 |

| 13 | 12 |

| 14 | 13 |

| 15 | 14 |

| 16 | 15 |

| 17 | 16 |

| 18 | 17 |

| 19 | 18 |

| 20 | 19 |

| 21 | 20 |

| 22 | 24 |

| 23 | 23 |

| 24 | 8 |


# 《修改对照表》

| 审查意见序号 | 问题摘要 | 核对结果 | 具体修改动作 | 修改位置 | 是否完成 | 备注 |
|---:|---|---|---|---|---|---|
| 1 | Introduction 首段编号制顺序倒置 | 经核对属实 | 按全文首次出现顺序重建 1–24 编号体系，并同步改写正文引文与文后参考文献顺序 | Introduction 首段；References 全节 | 是 | 旧 [5,7,8] / [1-4,24] 已改为新序列 |
| 2 | [6] 首次出现晚于 [7]/[8] | 经核对属实 | 通过全篇重编号消除首次出现逻辑倒置 | Introduction 首段 | 是 | 原 [5-8] 改为 **[1-3,9]** |
| 3 | 多处顺序倒置（[9,12-21]、[9-11,14-17]、[4,23]/[22]） | 经核对属实 | 全文统一重编号并同步修正压缩区间格式 | Introduction 第 2 段；Methods 2.8；Discussion | 是 | 不做局部修补 |
| 4 | Supplementary Figure 命名不一致 | 经核对属实 | 全文统一为 **Supplementary Figure S1–S3** | Methods 2.8；Results 3.5；Discussion；Appendix A | 是 | 附录题注全部改名 |
| 5 | Table 1–3 缺少正文明确调用 | 经核对属实 | 在相应方法/结果段落补入 **Table 1、Table 2、Table 3** 的自然调用 | 2.4；2.6；3.6 | 是 | 满足“先引后现” |
| 6 | Figure 1–8 缺少正文明确调用 | 经核对属实 | 在 2.1、3.1、3.3、3.4、3.6 补入 **Figure 1–8** 调用 | 2.1；3.1；3.3；3.4；3.6 | 是 | 满足“先引后现” |
| 7 | Supplementary Figure S1、S2 悬空 | 经核对属实 | 在 3.4 增补对 **Supplementary Figure S1** 与 **Supplementary Figure S2** 的调用 | Results 3.4；Appendix A captions | 是 | 不再悬空 |
| 8 | Figure 8 题注与图面严重不一致，占位图且缺 (b) | 经核对：上传 DOCX 中确为占位图；仓库中存在正式 Figure 8 | 用仓库正式 **fig8_literature_benchmark.png** 替换 DOCX 占位图，并同步调整 Figure 8 题注及 3.6 正文表述 | Figure 8 图像；Figure 8 caption；Results 3.6 | 是 | 已按正式双 panel 图修复 citeturn617926view0turn519538view0turn538128view0 |
| 9 | Figure 1(b) 图内硬编码 “Figs. 5–7” | 经核对属实 | 直接编辑内嵌 Figure 1 图像，将硬编码编号改为中性 **Summary** 标注 | Figure 1(b) 内嵌图像 | 是 | 避免再次引发编号冲突 |
| 10 | Table 3 跨页断裂、续表标识不足 | 当前 DOCX 表格数据完整；原 PDF 问题可复现于旧版排版 | 对 Table 3 设置表头重复与行不可跨页，并将题注与表格保持关联；另完成生成版 PDF 自检 | Table 3 表格对象 | 基本完成 | 当前修订稿导出 PDF 中 Table 3 未再断裂；期刊终排仍建议再校 |
| 11 | 作者截断规则不统一 | 经核对属实 | 在未获目标期刊体例前，统一为：**多作者条目采用 first author + et al.；单作者条目保留原样** | References 全节 | 是 | 采用内部一致性优先 |
| 12 | DOI 呈现不统一 | 经核对属实 | 统一 DOI 格式为 `doi:...`；补入可权威核实的 DOI；对无法可靠补入者不臆造 | References 全节 | 部分完成 | 已补核 Pennes、Wilson、Kotadia；Ref. 23 因书目信息冲突保留待核 citeturn458262search10turn932563search0turn714611view0turn842525search2 |
| 13 | 题名页作者/通讯作者占位语未清理 | 经核对属实 | 替换为显式占位标记 **[待作者补充作者与单位信息]**、**[待作者补充通讯作者信息]** | Title page | 是 | 未擅自补写实名信息 |
| 14 | Funding / Acknowledgements 占位语未清理 | 经核对属实 | 替换为显式占位标记 **[待作者补充 Funding statement]**、**[待作者补充 Acknowledgements]** | Funding；Acknowledgements | 是 | 未擅自补写声明 |


# 《待作者确认/补充事项》

1. **作者与单位信息**  
   当前原稿未提供真实作者姓名、单位与排序，因此只能保留 **[待作者补充作者与单位信息]**，不能直接补写。

2. **通讯作者信息**  
   当前原稿未提供通讯作者姓名、邮箱及单位，因此只能保留 **[待作者补充通讯作者信息]**。

3. **Funding statement**  
   原稿未提供真实基金项目名称、编号或“None/Not applicable”判定依据，因此只能保留 **[待作者补充 Funding statement]**。

4. **Acknowledgements**  
   原稿未提供可公开致谢对象或项目支持信息，因此只能保留 **[待作者补充 Acknowledgements]**。

5. **匿名投稿模板状态**  
   当前原稿包含“submission 前补全作者信息”式占位语，但无法仅凭现有材料判断目标期刊是否采用盲审匿名模板；请作者按目标期刊模板最终确认标题页呈现方式。

6. **Reference 23（Fahrenholtz SJ, et al.）书目信息/DOI 核对**  
   当前稿件条目为 `Int J Hyperthermia. 2014;30:54-63.`，但外部权威数据库检索到同标题记录为 `2013;29(4):324-35` 且 DOI 为 `10.3109/02656736.2013.798036`。由于用户明确要求不得擅自改动文献事实信息，因此本轮未直接改写该条完整书目信息，请作者核对原始来源后再定稿。 citeturn842525search2

7. **最终期刊排版复核（Table 3）**  
   本次修订稿已对 Table 3 设置“表头重复 + 行不可跨页”，并在本地导出 PDF 中核到该表未再拆行；但正式期刊模板重排后仍可能发生分页变化，作者需在投稿前最终 proof 再查一次。


# 《全篇一致性自检结果》

- **参考文献是否已按首次出现顺序重排：是。** 首次出现序列已重建为 1–24，且文后条目顺序同步更新。
- **是否仍存在倒置编号：否。** 重排后首次出现序列为严格递增。
- **Figure 1–8 是否均有正文明确调用：是。**
- **Table 1–3 是否均有正文明确调用：是。**
- **Supplementary Figure S1–S3 是否均已统一命名并有调用：是。**
- **Figure 8 是否仍存在未决问题：当前修订稿中否。** 占位图已替换为仓库正式图，并同步修正文题注与结果表述。作者仅需确认这是计划提交的最终版本。 citeturn617926view0turn519538view0turn538128view0
- **Table 3 是否仍需人工排版处理：原则上已处理，但终排 proof 仍建议人工复核。**
- **占位文本是否已清理为规范标记：是。**
- **作者截断规则是否已统一：是。** 当前统一为多作者条目 first author + et al.
- **DOI 呈现是否已统一：基本是。** 已有/已核实 DOI 统一为 `doi:...` 格式；未可靠核实者未臆造。
- **是否仍存在需要作者人工完成的事项：是。** 主要包括作者信息、通讯作者信息、Funding、Acknowledgements、匿名模板确认，以及 Ref. 23 的最终书目信息核对。
