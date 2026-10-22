# Related work (screened 2026-10-09)

Bottom line: many papers measure MLLM ECG **accuracy**, and some add **correct** clinical context.
None found gives a **wrong** hint on an ECG image. Medical-image sycophancy work skips ECG.

## Closest: clinical context changes MLLM ECG answers (correct context only)
- **Can J Cardiol 2025**, "Beyond Text" (10.1016/j.cjca.2025.01.036): GPT-4 on 150 ECGs.
  Accuracy was 19% without context and 45% with it; ACS went from 10% to 70%.
  This suggests the model reads the text more than the tracing, which is our core motivation.
- **BMC Emerg Med 2026** (10.1186/s12873-026-01486-y): custom "ECG Reader-GPT" vs 10 EM specialists on 72 ECGs.
  The GPT went from 24% to 27% with the history added; the specialists scored 77–79%.
- **Diagnostics 2026** (10.3390/diagnostics16030388): ChatGPT/Gemini/DeepSeek on Harrison's visual cases.
  Image only vs image plus history; ChatGPT went from 50.7% to 80.4%. These are not ECG-specific.

## Design precedent in another modality
- **JAAD 2026**, melanoma "framing bias" (10.1016/j.jaad.2026.03.056): prompt framing shifts ChatGPT's
  melanoma classification.
- **JAAD 2026 comment**, "The cost of AI sycophancy in dermoscopic diagnosis" (10.1016/j.jaad.2026.05.142).
- **EchoBench** (arXiv 2509.20146): 2,122 images, 20 modalities, **no ECG**. It uses patient, student and
  physician bias prompts. Metric: share of answers that match the wrong user opinion.

## ECG MLLM accuracy / reliability (background)
- Life 2026 (10.3390/life16040681, PMC13117897): 13 ECGs × 5 MLLMs, 2,275 assessments.
  Accuracy 52–65%; ST/T reading 20–41%. Covers inter-run reliability only, with no misleading context.
- J Electrocardiol 2026 (10.1016/j.jelectrocard.2026.154411): GPT-5.2 vs Gemini 3 Pro on axis/rhythm.
  Macro F1 was 45% and 32%.
- Heart and Lung 2026: GPT-5 vs GPT-4o for STEMI, compared with cardiologists and EM physicians.
- Resuscitation 2025 (10.1016/j.resuscitation.2025.110905): post-ROSC OMI. Chatbots had AUROC about 0.46,
  vs Queen of Hearts at 0.85.
- Resuscitation 2026 letter, "The siren song of the Chatbot" (10.1016/j.resuscitation.2026.110973):
  persuasive hallucinations and automation bias in OMI detection.
- LNCS 2027, "Same Models, Better Results" (10.1007/978-3-032-30813-9_18): 30-shot prompting.
  GPT-4o reached 81.6% on MI vs non-MI (n=928).
- ECG-R1 (ICML 2026, arXiv 2602.04279): measures how widespread hallucination is; does not test sycophancy.
- PULSE / ECGInstruct (npj Digit Med 2026): an ECG-specialised MLLM, a candidate comparison model.

## Design implications
1. Baseline accuracy is low, so measure flips only on cases the model gets right without a hint.
2. Correct context lifts ACS accuracy from 10% to 70% (Can J Cardiol). Run correct-hint and wrong-hint arms
   on the same cases to separate "uses context" from "obeys context".
3. Cite the JAAD melanoma study and EchoBench as the method lineage. Our contribution is ECG, STEMI stakes,
   and Thai-language prompts.

## Re-scan 2026-10-19 (Scopus + web; arXiv/medRxiv via web search)
Still no study of wrong hints / sycophancy on ECG images (Scopus q1 = 0; 10 new ECG+LLM papers, none on this).
Supporting work found:
- **ECG Mirage** (arXiv 2609.21755, Oxford): VLMs gain little from matched vs mismatched ECGs when predicting ICU
  admission or deterioration on MDS-ED ("ECG neglect / confusion"). Same motivation as ours (image under-used); different task. Verify the full text before citing.
- **MIRAGE: The Illusion of Visual Understanding** (arXiv 2603.21687): frontier models describe images never provided, including pathology-biased findings.
- Sycophancy in other visual domains: charts (ECCV 2026, Springer 10.1007/978-3-032-37271-0_26), video-LLMs (ACL 2026 long.369).
- New ECG+LLM accuracy papers: npj Digit Med 2026 ACS triage (10.1038/s41746-026-02904-y), AJEM 2026 medical VLM for acute coronary occlusion
  (10.1016/j.ajem.2026.09.054), J Nurse Pract 2026 ChatGPT 12-lead (10.1016/j.nurpra.2026.106012). These are accuracy studies only.
