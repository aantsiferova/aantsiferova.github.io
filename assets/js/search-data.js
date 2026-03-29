// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-publications",
          title: "publications",
          description: "Publications in reversed chronological order.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "Research projects in video quality assessment, adversarial robustness, and video compression.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "Anastasia Antsiferova&#39;s CV",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "news-i-was-honored-to-visit-the-msu-bit-engineering-department-in-shenzhen-china-as-an-invited-expert-to-deliver-a-research-talk-and-establish-a-framework-for-future-collaboration",
          title: 'I was honored to visit the MSU-BIT Engineering Department in Shenzhen, China as...',
          description: "",
          section: "News",},{id: "news-our-paper-about-leha-cvqad-dataset-for-video-quality-measurement-was-presented-by-my-phd-student-aleksandr-guschin-at-acm-international-conference-on-multimedia-acm-mm-2025-in-dublin-ireland",
          title: 'Our paper about LEHA-CVQAD dataset for video quality measurement was presented by my...',
          description: "",
          section: "News",},{id: "news-presented-our-paper-about-wibe-framework-for-image-watermarking-robustness-evaluation-as-a-demo-at-ieee-acm-international-conference-on-automated-software-engineering-ase-2025-in-seoul-south-korea",
          title: 'Presented our paper about WIBE framework for image watermarking robustness evaluation as a...',
          description: "",
          section: "News",},{id: "news-i-was-honored-to-receive-the-national-leaders-of-ai-award-for-top-3-young-scientific-leaders-in-russia-this-award-is-given-to-young-researchers-under-35-for-breakthrough-ai-solutions-specifically-focusing-on-those-publishing-at-top-tier-conferences-more-about-the-award-and-the-other-winners-here-https-ai-awards-ru-award-scientist",
          title: 'I was honored to receive the National “Leaders of AI” Award for top-3...',
          description: "",
          section: "News",},{id: "news-presented-our-paper-from-pixels-to-reality-physical-digital-patch-attacks-on-real-world-camera-as-a-demo-at-ieee-international-conference-on-pervasive-computing-and-communications-percom-2026-in-pisa-italy",
          title: 'Presented our paper “From Pixels to Reality: Physical-Digital Patch Attacks on Real-World Camera”...',
          description: "",
          section: "News",},{id: "projects-adversarially-robust-image-video-quality-assessment",
          title: 'Adversarially Robust Image/Video Quality Assessment',
          description: "Benchmarks and defense methods for image/video quality metrics robustness to adversarial attacks.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/adversarial_robustness/";
            },},{id: "projects-recognition-aware-video-quality-metrics",
          title: 'Recognition-Aware Video Quality Metrics',
          description: "Development of a new metric predicting object-detection accuracy for compressed videos, in collaboration with Huawei.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/recognition_aware_metrics/";
            },},{id: "projects-video-conferencing-quality-metrics",
          title: 'Video Conferencing Quality Metrics',
          description: "Methodology and dataset development for video-conferencing quality metrics, in collaboration with Huawei.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/video_conferencing/";
            },},{id: "projects-video-quality-metrics-benchmark",
          title: 'Video Quality Metrics Benchmark',
          description: "The largest benchmark of video-compression-related quality metrics, with industry-wide adoption.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/video_quality_benchmark/";
            },},{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/aantsiferova", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/anastasiaantsiferova", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=lJ-GGU8AAAAJ", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
