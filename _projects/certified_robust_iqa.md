---
layout: page
title: Certified and Robust-by-Design Quality Metrics
description: Provable robustness guarantees and robust architectures for image quality assessment models.
img:
importance: 3
category: research
related_publications: true
---

Empirical defenses can be broken by stronger attacks, so we develop quality metrics with guarantees. We started with robustness verification of no-reference image and video quality metrics {% cite vatolinTowards2024 %} and then proposed certified defenses based on randomized smoothing: median smoothing for blind IQA {% cite antsiferovaStochastic2025 %} and certified feature smoothing {% cite antsiferovaFsiqa2025 %}.

In parallel, we design architectures that are robust by construction: we studied which architectural choices make IQA models withstand adversarial perturbations {% cite vatolinRobustness2025 %}, proposed a cross-scale robust neck for no-reference IQA {% cite vatolinSpectral2026 %}, and the compact full-reference metric BiRQA with anchored adversarial training {% cite antsiferovaBirqa2026 %}.
