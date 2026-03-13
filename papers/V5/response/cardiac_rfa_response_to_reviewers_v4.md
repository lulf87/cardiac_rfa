# Response to Reviewer (Major Revision)

We thank the reviewer for the careful, constructive, and technically informed assessment of our manuscript. We agree that the earlier draft was not yet sufficiently complete or methodologically explicit for formal submission. In the revised manuscript, we addressed manuscript completeness, expanded the mathematical and numerical description, strengthened the uncertainty-quantification section, clarified the interpretation of vHPSD-related findings, added lesion-width and lesion-area metrics, and replaced the previous Figure 8 placeholder with a populated literature-derived trend benchmark.

## 1. Manuscript completeness and placeholder content
**Reviewer comment:** The manuscript was incomplete and still contained placeholder material, including author metadata and a Figure 8 template.

**Response:** We agree. All placeholder content has been removed from the scientific body of the manuscript. Figure 8 is now populated with a literature-derived protocol-level benchmark rather than a template. The remaining placeholders are limited to author metadata, funding, acknowledgements, and conflict-of-interest declarations, which are author-supplied administrative items to be finalized prior to submission.

## 2. Reproducibility of the computational model
**Reviewer comment:** The Methods section was too brief to ensure reproducibility.

**Response:** We agree and substantially expanded the Methods section. The revised version now explicitly states the governing equations for the quasi-static electrical problem, transient bioheat problem, and Arrhenius damage model; the geometric dimensions of the electrode-blood-myocardium configuration; boundary and initial conditions; material properties; protocol implementation; and the numerical settings used for grid, time-step, and solver selection. A revised solver/UQ settings table has also been added.

## 3. Underdescribed and apparently undersampled uncertainty quantification
**Reviewer comment:** The UQ section lacked distributions, sample counts, independence assumptions, and convergence/uncertainty information, while the probability maps suggested very low sample counts.

**Response:** We agree. The revised manuscript now explicitly reports the uncertain variables, their truncated-normal assumptions, the support ranges, the nominal means, and the use of stratified sampling. The paper-level uncertainty maps were regenerated with 64 samples per nominal cell, replacing the earlier exploratory low-sample maps. We now report 95% Wilson-score confidence intervals for transmurality and overheating probabilities and include a supplementary summary figure of CI half-widths. In the revised results, the median CI half-width is 0.028 for both transmurality and overheating probability, with maxima of 0.113 and 0.119, respectively.

## 4. External benchmark too weak
**Reviewer comment:** The literature-derived benchmark was incomplete and too limited.

**Response:** We agree that the external benchmark remains limited and should not be interpreted as strict validation. Figure 8 has been populated with protocol-matched literature depth values and is now framed explicitly as a trend-level benchmark rather than a geometry-matched validation. The revised manuscript states that the reduced model reproduces the protocol-level ranking while underestimating the absolute lesion depth under the nominal setup.

## 5. Interpretation of vHPSD
**Reviewer comment:** The interpretation of vHPSD was too strong.

**Response:** We agree and softened the language throughout the manuscript. The revised text consistently states that the conclusions regarding vHPSD are model-based findings under the present reduced 2D electro-thermal assumptions and do not constitute general clinical claims.

## 6. Output metrics were biased toward depth and transmurality
**Reviewer comment:** The outputs emphasized depth-related quantities and should include additional lesion-geometry metrics.

**Response:** We agree. The revised workflow now reports maximum lesion width, lesion area, and depth-to-width ratio in addition to lesion depth, depth fraction, transmurality, and peak temperature. The revised deterministic summary figure has been expanded accordingly.

## 7. Novelty should rely on methodological value rather than expected depth ranking
**Reviewer comment:** The depth ranking itself is not novel; the methodological contribution must be better justified.

**Response:** We agree. The revised manuscript more clearly emphasizes that the contribution lies in the reduced-complexity uncertainty-aware framework and its use for comparative transmurality/overheating risk mapping across wall thickness, contact, and cooling conditions.

## 8. Number of references was insufficient
**Reviewer comment:** The reference list was too small.

**Response:** We agree and expanded the reference list to better situate the study within the RF cardiac ablation modeling literature, including classic bioheat and thermal-injury references as well as protocol-comparison studies relevant to HPSD and vHPSD.

## Summary
We appreciate the reviewer’s assessment and agree that the earlier draft was not yet suitable for submission. The revised version strengthens manuscript completeness, methodological reproducibility, uncertainty quantification transparency, lesion-geometry reporting, and benchmark reporting. We believe these revisions materially improve the manuscript and better position it as a methodology-focused computational modeling study.
