insert into public.products (id, title, category, price_usd, price_band, tags, risk_flags, content_type, lifecycle_hint, supply_chain, content_play)
values
  ('11111111-1111-1111-1111-111111111111', '自清洁洗脸刷', 'Beauty', 24.9, '20-30', array['美妆工具','清洁'], array['易退货'], 'template_script', 'mid',
    '{"cost_usd":6,"weight_kg":0.4,"fragile":false,"battery":false,"hazmat":false,"lead_time_days":12,"moq":200}',
    '{"hook_type":"前后对比","demo_style":"真人上脸","emotion_type":"爽感","ugc_difficulty":"低","script_template":"10秒见证变化"}'),
  ('22222222-2222-2222-2222-222222222222', '便携迷你热风梳', 'Beauty', 39.0, '30-50', array['美发','高客单'], array['易损坏'], 'human_driven', 'short',
    '{"cost_usd":12,"weight_kg":0.6,"fragile":true,"battery":false,"hazmat":false,"lead_time_days":18,"moq":300}',
    '{"hook_type":"出门急救","demo_style":"真人梳理","emotion_type":"省时","ugc_difficulty":"中","script_template":"3分钟造型"}'),
  ('33333333-3333-3333-3333-333333333333', '宠物智能喂食器', 'Pet', 65.0, '50-80', array['智能设备','宠物刚需'], array['电池合规'], 'ad_scalable', 'long',
    '{"cost_usd":25,"weight_kg":1.2,"fragile":false,"battery":true,"hazmat":false,"lead_time_days":25,"moq":500}',
    '{"hook_type":"主人不在家","demo_style":"远程操控","emotion_type":"安心","ugc_difficulty":"高","script_template":"出差也能喂"}'),
  ('44444444-4444-4444-4444-444444444444', '厨房多功能切菜器', 'Home', 19.0, '10-20', array['厨房刚需','快消'], array['锋利'], 'template_script', 'long',
    '{"cost_usd":5,"weight_kg":0.8,"fragile":false,"battery":false,"hazmat":false,"lead_time_days":10,"moq":200}',
    '{"hook_type":"切菜慢","demo_style":"快速演示","emotion_type":"效率","ugc_difficulty":"低","script_template":"30秒切丝"}'),
  ('55555555-5555-5555-5555-555555555555', '解压筋膜枪', 'Fitness', 49.0, '40-60', array['运动恢复','礼品'], array['电池合规'], 'ad_scalable', 'mid',
    '{"cost_usd":18,"weight_kg":0.9,"fragile":false,"battery":true,"hazmat":false,"lead_time_days":20,"moq":400}',
    '{"hook_type":"上班久坐","demo_style":"痛点场景","emotion_type":"放松","ugc_difficulty":"中","script_template":"一按就松"}'),
  ('66666666-6666-6666-6666-666666666666', '可折叠收纳盒', 'Home', 14.0, '10-20', array['收纳','复购'], array['低风险'], 'template_script', 'long',
    '{"cost_usd":3,"weight_kg":0.5,"fragile":false,"battery":false,"hazmat":false,"lead_time_days":8,"moq":150}',
    '{"hook_type":"桌面混乱","demo_style":"整理前后","emotion_type":"满足","ugc_difficulty":"低","script_template":"5分钟整洁"}'),
  ('77777777-7777-7777-7777-777777777777', '户外便携净水壶', 'Outdoor', 55.0, '50-80', array['户外','功能性'], array['滤芯合规'], 'human_driven', 'mid',
    '{"cost_usd":20,"weight_kg":0.7,"fragile":false,"battery":false,"hazmat":false,"lead_time_days":16,"moq":250}',
    '{"hook_type":"野外口渴","demo_style":"现场过滤","emotion_type":"安全","ugc_difficulty":"中","script_template":"5秒净水"}'),
  ('88888888-8888-8888-8888-888888888888', '智能猫砂盆', 'Pet', 220.0, '200+', array['高客单','懒人经济'], array['物流成本高','电池合规'], 'ad_scalable', 'long',
    '{"cost_usd":90,"weight_kg":8.5,"fragile":true,"battery":true,"hazmat":false,"lead_time_days":30,"moq":200}',
    '{"hook_type":"自动清理","demo_style":"对比传统猫砂","emotion_type":"解放双手","ugc_difficulty":"高","script_template":"每天省20分钟"}'),
  ('99999999-9999-9999-9999-999999999999', '无火香薰扩香仪', 'Home', 32.0, '30-50', array['香氛','礼品'], array['易碎'], 'human_driven', 'mid',
    '{"cost_usd":9,"weight_kg":0.6,"fragile":true,"battery":false,"hazmat":false,"lead_time_days":14,"moq":300}',
    '{"hook_type":"房间异味","demo_style":"香氛覆盖","emotion_type":"治愈","ugc_difficulty":"低","script_template":"30秒去味"}'),
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '旅行压缩收纳袋', 'Travel', 18.0, '10-20', array['旅行必备','高复购'], array['低风险'], 'template_script', 'long',
    '{"cost_usd":4,"weight_kg":0.3,"fragile":false,"battery":false,"hazmat":false,"lead_time_days":9,"moq":200}',
    '{"hook_type":"行李爆满","demo_style":"压缩对比","emotion_type":"惊喜","ugc_difficulty":"低","script_template":"立刻省50%空间"}');

insert into public.product_cards (product_id, why_fit, first_test, stop_loss)
values
  ('11111111-1111-1111-1111-111111111111', '低客单、内容脚本好做，适合内容团队快速复制。', '用真人洗脸前后对比做 5 条短视频，测转化率。', '退货率超过 12% 或差评集中在刷头掉毛则停。'),
  ('22222222-2222-2222-2222-222222222222', '美发痛点强，但易损需控售后，适合有达人配合。', '找 10 位达人做出门急救场景短视频。', '损坏投诉超过 8% 或物流破损率过高时停。'),
  ('33333333-3333-3333-3333-333333333333', '高客单+智能设备适合投流放大，强调远程安心。', '测试高意向人群投流，观察 ROI 和评论。', '合规审查卡住或投流 ROI 连续两周 < 1 停。'),
  ('44444444-4444-4444-4444-444444444444', '厨房刚需低风险，适合新手稳定跑。', '拍 8 条 30 秒切菜效率视频，测试互动率。', '点击率低于 0.8% 或退货率持续升高停。'),
  ('55555555-5555-5555-5555-555555555555', '适合投流或达人矩阵，主打放松场景。', '用痛点场景投流小预算测 7 天。', '电池合规或物流问题导致退货率上升时停。'),
  ('66666666-6666-6666-6666-666666666666', '供应链简单、低风险，适合内容模板批量复制。', '做整理前后对比视频，测试 5 个场景。', '转化率低于 1% 且评论集中吐槽材质时停。'),
  ('77777777-7777-7777-7777-777777777777', '功能性强，需强调安全与场景，适合达人种草。', '投放户外达人测 10 条场景内容。', '平台合规审查频繁或物流时效拖慢时停。'),
  ('88888888-8888-8888-8888-888888888888', '高客单 + 重货，适合现金流充足且投流团队。', '先投 3 组高意向广告，观察转化与咨询率。', '物流破损率超过 5% 或售后成本过高停。'),
  ('99999999-9999-9999-9999-999999999999', '治愈类情绪产品，适合内容讲故事。', '做氛围感短视频测试 7 天。', '破损率高或差评集中在漏液时停。'),
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '旅行刚需且复购高，适合新手跑量。', '用收纳前后对比视频测试 10 条。', '互动率低且评论质疑效果时停。');

insert into public.rules (tier, priority, condition, filter, public_reason_title, public_reason_detail, is_active)
values
  ('forbidden', 1, '{"maxRisk":40}', '{"priceBand":["200+"],"riskFlagsAny":["物流成本高"]}', '高客单重货不适合低风险阶段', '高客单+重货意味着试错成本高，你目前风险承受度偏低。', true),
  ('not_recommended', 2, '{"maxCash":50}', '{"contentType":["ad_scalable"],"priceUsdMin":60}', '现金流不足支撑投流放量', '放量类产品需要持续资金，你当前现金流偏谨慎。', true),
  ('not_recommended', 3, '{"maxContent":50}', '{"contentType":["human_driven"],"tagsAny":["高客单"]}', '内容能力不足以支撑高客单讲解', '高客单需要强说服力内容，你当前内容能力偏保守。', true),
  ('testable', 5, '{"minRisk":45}', '{"priceBand":["30-50","50-80"],"tagsAny":["功能性","美发","运动恢复"]}', '有一定试错空间可测试功能型产品', '你有一定风险承受度，可以小批量测试功能性产品。', true),
  ('recommended', 6, '{"minContent":55}', '{"contentType":["template_script"],"priceBand":["10-20","20-30"],"riskFlagsAny":["低风险"]}', '内容模板适合稳定复制', '你内容能力偏强，低风险模板产品更容易稳定出量。', true),
  ('recommended', 7, '{"minScale":55}', '{"contentType":["ad_scalable"],"priceBand":["50-80"],"tagsAny":["功能性"]}', '具备放量能力的功能型产品', '你具备放量能力，功能型产品适合用数据放大。', true),
  ('testable', 8, '{"minContent":50}', '{"contentType":["human_driven"],"priceBand":["30-50"],"tagsAny":["礼品"]}', '情绪型产品可用达人内容测试', '你能产出一定内容，可用达人故事测试情绪类产品。', true),
  ('forbidden', 9, '{"maxRisk":45}', '{"riskFlagsAny":["电池合规"]}', '合规风险对新手过高', '电池类产品合规风险高，容易卡在平台审核。', true),
  ('testable', 10, '{"minScale":45}', '{"category":["Home","Travel"],"priceBand":["10-20"]}', '低客单生活品适合规模化复制', '低客单生活品可通过规模化内容复制放量。', true),
  ('recommended', 11, '{"minContent":45,"maxRisk":70}', '{"tagsAny":["旅行必备","收纳"],"priceBand":["10-20"]}', '旅行收纳品适合稳健增长', '你偏稳健节奏，收纳类容易稳定转化。', true);
