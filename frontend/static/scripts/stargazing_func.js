/**
 * 计算观星指数 (0%-100%，百分比越高越适合观星)
 * @param {Object} weatherData - 气象数据对象
 * @param {number} sqmValue - SQM值 (mag/arcsec²)，数值越高光污染越少
 * @returns {Object} 包含观星指数(百分比)和各维度评分的结果对象
 */
function calculateStargazingIndex(weatherData, sqmValue) {
    // 初始化各维度得分 (总分100分，按权重分配)
    let score = {
        total: 0,          // 最终观星指数(百分比)
        weather: 0,        // 天气得分 (权重30)
        moonlight: 0,      // 月光得分 (权重30)
        visibility: 0,     // 能见度得分 (权重20)
        lightPollution: 0  // 光污染(SQM)得分 (权重20)
    };

    // ---------------------- 1. 天气评分 (0-30分) ----------------------
    const weatherText = weatherData.textNight;
    const precip = parseFloat(weatherData.precip || 0);

    if (precip > 0) {
        score.weather = 0; // 有降水，完全不适合
    } else if (weatherText.includes('晴')) {
        score.weather = 30; // 晴天，满分
    } else if (weatherText.includes('多云') || weatherText.includes('少云')) {
        score.weather = 20; // 多云，较好
    } else if (weatherText.includes('阴')) {
        score.weather = 10; // 阴天，较差
    } else {
        score.weather = 0; // 其他恶劣天气
    }

    // ---------------------- 2. 月光评分 (0-30分) ----------------------
    const moonPhase = weatherData.moonPhase || '';
    const moonrise = weatherData.moonrise || '';
    const moonset = weatherData.moonset || '';
    const sunset = weatherData.sunset || '';
    const sunrise = weatherData.sunrise || '';

    // 月相对观星的影响 (新月最佳，满月最差)
    let moonPhaseScore = 0;
    if (moonPhase.includes('新月')) {
        moonPhaseScore = 30;
    } else if (moonPhase.includes('残月') || moonPhase.includes('娥眉月')) {
        moonPhaseScore = 25;
    } else if (moonPhase.includes('上弦月') || moonPhase.includes('下弦月')) {
        moonPhaseScore = 15;
    } else if (moonPhase.includes('盈凸月') || moonPhase.includes('亏凸月')) {
        moonPhaseScore = 10;
    } else if (moonPhase.includes('满月')) {
        moonPhaseScore = 0;
    }

    // 月亮是否在夜间出现 (日落-日出期间)
    let moonInNight = true;
    if (moonset && sunset && timeToMinutes(moonset) < timeToMinutes(sunset)) {
        // 月亮在日落前落下
        moonInNight = false;
    } else if (moonrise && sunrise && timeToMinutes(moonrise) > timeToMinutes(sunrise)) {
        // 月亮在日出后升起
        moonInNight = false;
    }

    // 最终月光得分 (月亮不在夜间则满分，否则按月相评分)
    score.moonlight = moonInNight ? moonPhaseScore : 30;

    // ---------------------- 3. 能见度评分 (0-20分) ----------------------
    const vis = parseFloat(weatherData.vis || 0); // 能见度(km)
    const cloud = parseFloat(weatherData.cloud || 100); // 云量(%)
    const humidity = parseFloat(weatherData.humidity || 100); // 湿度(%)

    // 能见度得分 (越高越好，10km以上得满分10分)
    let visScore = Math.min(vis / 10, 1) * 10;
    // 云量得分 (越低越好，无云得满分10分，满云得0分)
    let cloudScore = Math.max(1 - cloud / 100, 0) * 10;
    // 湿度惩罚 (湿度>70%开始扣分，湿度100%扣完所有分)
    let humidityPenalty = Math.max(0, (humidity - 70) / 30);

    score.visibility = (visScore + cloudScore) * (1 - humidityPenalty);

    // ---------------------- 4. 光污染(SQM)评分 (0-20分) ----------------------
    // SQM值标准化评分 (基于专业观星SQM分级标准)
    if (sqmValue >= 21.7) {
        score.lightPollution = 20; // 暗夜天空，满分
    } else if (sqmValue >= 20.0) {
        score.lightPollution = 16; // 乡村天空，良好
    } else if (sqmValue >= 18.0) {
        score.lightPollution = 10; // 郊区天空，一般
    } else if (sqmValue >= 16.0) {
        score.lightPollution = 4; // 城市天空，较差
    } else {
        score.lightPollution = 0; // 市中心，极差
    }

    // ---------------------- 计算总分(百分比) ----------------------
    const totalScore = score.weather + score.moonlight + score.visibility + score.lightPollution;
    // 转换为百分比并保留1位小数，确保在0%-100%范围内
    score.total = parseFloat(Math.max(0, Math.min(100, totalScore)).toFixed(1));

    return score;
}

/**
 * 辅助函数：将时间字符串(HH:MM)转换为分钟数，便于比较
 * @param {string} timeStr - 时间字符串，如 "17:48"
 * @returns {number} 转换后的分钟数
 */
function timeToMinutes(timeStr) {
    if (!timeStr || timeStr === '') return 0;
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

// ---------------------- 使用示例 ----------------------
// 你的测试气象数据
const weatherData = {
    "fxDate": "2025-12-27",
    "sunrise": "07:03",
    "sunset": "17:48",
    "moonrise": "11:52",
    "moonset": "",
    "moonPhase": "上弦月",
    "moonPhaseIcon": "802",
    "tempMax": "20",
    "tempMin": "12",
    "iconDay": "100",
    "textDay": "晴",
    "iconNight": "150",
    "textNight": "晴",
    "wind360Day": "0",
    "windDirDay": "北风",
    "windScaleDay": "1-3",
    "windSpeedDay": "3",
    "wind360Night": "0",
    "windDirNight": "北风",
    "windScaleNight": "1-3",
    "windSpeedNight": "3",
    "humidity": "75",
    "precip": "0.0",
    "pressure": "1011",
    "vis": "25",
    "cloud": "2",
    "uvIndex": "4"
};
