---
layout: page
title: Hacking and Stabilizing VMAF
description: Analysis of how video preprocessing can artificially increase VMAF, the industry-standard video quality metric, and a stable modification of it.
img:
importance: 9
category: research
related_publications: true
---

VMAF is widely used to compare and tune video codecs, so its vulnerabilities directly affect industry decisions. We showed that simple color and contrast adjustments can artificially increase VMAF {% cite vatolinHacking2019 %}, and that both VMAF and its "no enhancement gain" version VMAF NEG are vulnerable to various preprocessing methods {% cite vatolinHacking2021 %}. We also developed a neural preprocessing method that increases VMAF via distillation {% cite galaktionovDevelopment2023 %}.

Building on this analysis, we proposed evolutionary and distillation-based adversarial attacks on VMAF and Stable VMAF, a modification that is substantially more robust to such manipulations {% cite vatolinStable2025 %}.
