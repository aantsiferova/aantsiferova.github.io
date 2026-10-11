---
layout: page
title: Adversarial Attacks on Image/Video Quality Metrics
description: New attacks and a large-scale benchmark revealing vulnerabilities of learning-based image and video quality metrics.
img:
importance: 2
category: research
related_publications: true
---

**Role:** Project Head | **Period:** Apr 2022 -- Dec 2024

Learning-based image and video quality metrics are used to tune codecs and train enhancement models, which makes them a target: a model can learn to "hack" the metric instead of improving perceived quality. We developed a family of white-box and black-box attacks on no-reference metrics — universal perturbations {% cite vatolinUniversal2022 %}, fast CNN-based attacks {% cite vatolinFast2023 %}, the invisible one-iteration IOI attack {% cite vatolinIoi2024 %}, and transferable cross-modal image-to-video attacks {% cite vatolinCrossmodal2025 antsiferovaImproving2026 %}.

Using these attacks, we built a benchmark of metrics robustness {% cite vatolinComparing2024 %}, which found vulnerabilities in 15 no-reference metrics and the current full-reference SOTA method.

**Project page:** [videoprocessing.ai/benchmarks/metrics-robustness.html](https://videoprocessing.ai/benchmarks/metrics-robustness.html)
