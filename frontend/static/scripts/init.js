// 初始化城市名称和输入框
// import axios from "axios";
// import axios from "axios";

const city_name = document.getElementById("city-name");
const city_input = document.getElementById("city-input");
const search_icon = document.getElementById("search-icon");
const error_toast = document.getElementById("error-toast");

// 初始化天气面板
const temp = document.getElementById("temp");
const weather_icon = document.getElementById("weather-icon");
const weather_condition_text = document.getElementById("weather-condition-text");
const humidity = document.getElementById("humidity");
const air_pressure = document.getElementById("air-pressure");
const visibility = document.getElementById("visibility");
const wind_speed = document.getElementById("wind-speed");
const wind_direction = document.getElementById("wind-direction");
const cloudiness = document.getElementById("cloudiness");
const uv_index = document.getElementById("uv-index");
const time = document.getElementById("time");
const day_temp = document.getElementById("day-temp");

// 初始化天文面板
const observing_index_level = document.getElementById("observing-index-level");
const today_index_level = document.getElementById("today-observing-index-level");
const tomorrow_index_level = document.getElementById("tomorrow-observing-index-level");
const two_days_index_level = document.getElementById("two-days-observing-index-level");


const observing_index = document.getElementById("observing-index");
const today_index = document.getElementById("today-observing-index");
const tomorrow_index = document.getElementById("tomorrow-observing-index");
const two_days_index = document.getElementById("two-days-observing-index");


// 初始化侧边栏
const moon_phase = document.getElementById("moon-phase");
const moon_phase_time = document.getElementById("moon-phase-time");
const moon_icon = document.getElementById("moon-icon");
const light_harm_level = document.getElementById("light-harm-level");
const light_harm_type = document.getElementById("light-harm-type");
const light_harm_sqm = document.getElementById("light-harm-sqm");

const api_url = "/api/";

// 封装print函数
function print(message) {
    console.log(message);
}


/**
 * 将ISO 8601格式时间转换为 (YYYY-MM-DD HH时) 格式
 * @param {string} isoTimeStr - 待转换的ISO时间字符串（如2025-12-27T11:00+08:00）
 * @param {boolean} [padHour=true] - 小时是否补零（true=补零，如09时；false=不补零，如9时）
 * @returns {string} 转换后的易读时间（失败返回空字符串）
 */
function format_time(isoTimeStr, padHour = true) {
    // 补零工具函数（内部封装，不对外暴露）
    const padZero = (num) => num.toString().padStart(2, '0');

    try {
        // 1. 解析ISO时间（自动识别+08:00时区）
        const date = new Date(isoTimeStr);
        // 校验时间是否有效（避免传入非法字符串）
        if (isNaN(date.getTime())) {
            console.error('格式转换失败：传入的时间字符串无效 →', isoTimeStr);
            return '';
        }

        // 2. 提取时间字段
        const year = date.getFullYear();
        const month = padZero(date.getMonth() + 1); // 月份0开始，+1后补零
        const day = padZero(date.getDate());
        const hour = padHour ? padZero(date.getHours()) : date.getHours();

        // 3. 拼接目标格式
        return `${year}-${month}-${day} ${hour}时`;
    } catch (error) {
        // 捕获所有异常，避免程序崩溃
        console.error('时间转换出错：', error.message);
        return '';
    }
}

// TODO: 获取当前时间（格式化）
function getCurrentTimeWithFormat() {
    // 1. 获取原生时间数据（核心）
    const now = new Date();
    const rawData = {
        timestamp: now.getTime(), // 毫秒时间戳
        year: now.getFullYear(),
        month: now.getMonth() + 1,
        day: now.getDate(),
        hour: now.getHours(),
        minute: now.getMinutes(), // 保留原始分钟（可备用）
        second: now.getSeconds()
    };

    // 2. 格式化：分钟固定00，补0处理
    const formatted = `${rawData.year}-${String(rawData.month).padStart(2, "0")}-${String(rawData.day).padStart(2, "0")}T${String(rawData.hour + 1).padStart(2, "0")}:00+08:00`;

    return {rawData, formatted};
}

/**
 * 将SQM转换为波特尔光害指数（严格匹配天文通字段：极暗/很暗/较暗/尚暗/中等/较亮/很亮/极亮/极亮）
 * @param {number} sqmValue - SQM值（单位：mag/arcsec²）
 * @returns {Object} 转换结果：有效状态/等级/天文通名称/描述
 */
function convertSqmToBortle(sqmValue) {
    // 核心映射：波特尔等级 1-9 → 天文通名称（严格按你给的顺序）
    const BORTLE_NAME_MAP = {
        1: '极暗',
        2: '很暗',
        3: '较暗',
        4: '尚暗',
        5: '中等',
        6: '较亮',
        7: '很亮',
        8: '极亮',
        9: '极亮'
    };

    // 等级描述（可选保留，不影响字段）
    const DESC_MAP = {
        1: '银河中心细节清晰，观星最佳环境',
        2: '银河轮廓清晰，大量暗星可见',
        3: '银河仍明显，部分暗星被遮挡',
        4: '银河可见但亮度降低',
        5: '银河暗淡，仅亮部可见',
        6: '银河几乎不可见，光污染明显',
        7: '仅能看到亮银河，大量光害',
        8: '银河不可见，仅亮星可见',
        9: '仅能看到最亮的几颗星，重度光污染'
    };

    // 输入验证
    if (typeof sqmValue !== 'number' || isNaN(sqmValue)) {
        return {
            valid: false,
            error: 'SQM值必须是有效数字（如 17.87）',
            bortleLevel: null,
            name: null,
            description: null,
            originalSqm: sqmValue
        };
    }

    // 波特尔等级判断（SQM范围不变）
    let bortleLevel;
    if (sqmValue >= 21.7) bortleLevel = 1;
    else if (sqmValue >= 21.3) bortleLevel = 2;
    else if (sqmValue >= 20.8) bortleLevel = 3;
    else if (sqmValue >= 20.4) bortleLevel = 4;
    else if (sqmValue >= 19.8) bortleLevel = 5;
    else if (sqmValue >= 19.2) bortleLevel = 6;
    else if (sqmValue >= 18.4) bortleLevel = 7;
    else if (sqmValue >= 17.5) bortleLevel = 8;
    else bortleLevel = 9;

    // 返回结果（name字段完全匹配你给的列表）
    return {
        valid: true,
        error: null,
        bortleLevel: bortleLevel,
        name: BORTLE_NAME_MAP[bortleLevel],
        description: DESC_MAP[bortleLevel],
        originalSqm: sqmValue
    };
}

// TODO: 获取用户地理位置
async function get_geolocation() {
    const token = '01e69e5e06e633'; // 注册获取
    const response = await fetch(`https://ipinfo.io/json?token=${token}`);
    const data = await response.json();
    // loc字段为"纬度,经度"
    // print(data)
    const [lat, lon] = data["loc"].split(',').map(Number);
    return {
        ip: data.ip,
        city: data.city,
        region: data.region,
        coordinates: {lat, lon},
        isp: data["org"]
    };
}

// TODO: 渲染实时天气数据
async function render_hourly_data(params) {
    try {
        const response = await axios.get(api_url + "hourly_data", {params: params});
        const data = response.data;
        // 访问正确, 更新实时天气数据
        if (data.code === "200") {
            // 更新实时天气数据
            let present_data = null;
            for (let i = 0; i < data["hourly"].length; i++) {
                if (data["hourly"][i]["fxTime"] === getCurrentTimeWithFormat().formatted) {
                    present_data = data["hourly"][i];
                    print(i)
                    break;
                } else if (api_url === "/test/") {
                    present_data = data["hourly"][0];
                }
            }
            // let present_data = data["hourly"][0];
            // 获取值
            let time_data = present_data["fxTime"];
            let temp_data = present_data["temp"];
            let weather_data = present_data["text"];
            let wind_speed_data = present_data["windSpeed"];
            let air_pressure_data = present_data["pressure"];
            let cloudiness_data = present_data["cloud"];
            let humidity_data = present_data["humidity"];
            let weather_icon_data = present_data["icon"];
            let wind_direction_data = present_data["windDir"];
            // 格式化时间
            time_data = format_time(time_data);
            // 更新页面元素
            // 更新时间
            time.textContent = time_data;
            // 更新温度
            temp.innerHTML = `${temp_data}<span style="font-size: 20px; margin-left: 5px;">℃</span>`;

            // 更新风速
            wind_speed.textContent = wind_speed_data + " m/s";
            // 更新气压
            air_pressure.textContent = air_pressure_data + " hPa";
            // 更新云量
            cloudiness.textContent = cloudiness_data + " %";
            // 更新湿度
            humidity.innerText = humidity_data + " %";
            // 更新天气图标
            weather_icon.className = `qi-${weather_icon_data}-fill`;
            // 更新风向
            wind_direction.textContent = wind_direction_data;
            // 更新天气情况
            weather_condition_text.textContent = weather_data;
        }
    } catch (error) {
        console.error(error);
    }
}

// TODO: 渲染日天气数据
async function render_day_data(params) {
    try {
        const response = await axios.get(api_url + "day_data", {params: params});
        const data = response.data;
        // 访问正确, 更新日天气数据
        if (data.code === "200") {
            let day_data = data["daily"][0];
            moon_phase.innerText = day_data["moonPhase"];
            moon_icon.className = `qi-${day_data["moonPhaseIcon"]}`;
            moon_phase_time.innerHTML = `月升:&nbsp${day_data["moonrise"]}<br>月落:&nbsp;${day_data["moonset"]}`;
            uv_index.textContent = day_data["uvIndex"];
            visibility.innerText = day_data["vis"] + " km";
            day_temp.textContent = `${day_data["tempMin"]} ~ ${day_data["tempMax"]} °C`;
        }
    } catch (error) {
        console.error(error);
    }
}

// TODO: 渲染光害数据
async function render_light_pollution_data(params) {
    try {
        const response = await axios.get(api_url + "light_pollution", {params: params});
        const data = response.data;
        // 访问正确, 更新光害数据
        let converted_data = convertSqmToBortle(data["brightness"]["mpsas"]);
        light_harm_level.innerText = `🌍 波特尔光害: ${converted_data["bortleLevel"]}级`;
        light_harm_type.innerText = `光害程度: ${converted_data["name"]}`;
        light_harm_sqm.innerText = `SQM值: ${converted_data["originalSqm"].toFixed(2)}`;

    } catch (error) {

        console.error(error);
    }
}

// TODO: 渲染位置数据
async function render_loc_data(params) {
    try {
        const response = await axios.get(api_url + "loc_data", {params: params});
        const data = response.data;
        console.log(data)
        // 访问正确, 更新位置数据
        if (data.code === "200") {
            print(data)
            let loc_data = data["location"][0];
            city_name.textContent = loc_data["name"];
            return {
                name: loc_data["name"],
            }
        } else if (data.code === "400") {
            show_error_toast("城市不存在或数据格式错误，请重试！");
        }

    } catch (error) {
        console.error(error);
    }
}

// TODO: 处理搜索按钮点击事件
async function handle_search() {
    // print("点击搜索按钮")
    const city_name = city_input.value.trim();
    if (!city_name) {
        error_toast.textContent = "请输入城市名称";
        show_error_toast("请输入城市名称");
        return;
    }
    city_input.value = ''
    let params = {
        city: city_name
    }
    try {
        render_loc_data(params).then(
            () => {
                print('更新城市为: ' + city_name)
            }
        );
        render(params);
    } catch (error) {
        show_error_toast('网络异常或城市不存在，请重试！');
        console.error(error);
    }

}

// 错误提示框定时器变量
let toast_timer = null;

// TODO: 显示错误提示框（自动消失，不影响其他元素）
function show_error_toast(text) {
    if (toast_timer) {
        clearTimeout(toast_timer);
    }
    error_toast.textContent = text;
    error_toast.style.opacity = '1';
    error_toast.style.visibility = 'visible';

    toast_timer = setTimeout(() => {
        print('隐藏错误提示框')
        error_toast.style.opacity = '0';
        error_toast.style.visibility = 'hidden';
        // 清空定时器变量，避免内存泄漏
        toast_timer = null;
    }, 3000);
}

// TODO: 计算观星指数描述
function calc_index_level(index) {
    if (index >= 80) {
        return ["极佳", "terrific"];
    } else if (index >= 60) {
        return ["一般", "average"];
    } else {
        return ["糟糕", "terrible"];
    }
}

// TODO: 渲染观星指数
async function render_stargazing_index(params) {
    // 渲染今日观星指数
    let response = await axios.get(api_url + "day_data", {params: params});
    let data = response.data;
    print(data)
    const sqm_data = document.getElementById("light-harm-sqm").innerText.replace("SQM值: ", "");
    // 访问正确, 更新观星指数数据
    let stargazing_index_today = calculateStargazingIndex(data["daily"][0], parseFloat(sqm_data));
    observing_index.innerHTML = `${stargazing_index_today.total.toFixed(0)}<span> %</span>`;
    today_index.innerHTML = `${stargazing_index_today.total.toFixed(0)}`;
    // 渲染明日观星指数
    let stargazing_index_tomorrow = calculateStargazingIndex(data["daily"][1], parseFloat(sqm_data));
    tomorrow_index.innerHTML = `${stargazing_index_tomorrow.total.toFixed(0)}`;
    // 渲染后日观星指数
    let stargazing_index_two_days = calculateStargazingIndex(data["daily"][2], parseFloat(sqm_data));
    two_days_index.innerHTML = `${stargazing_index_two_days.total.toFixed(0)}`;
    // 根据观星指数更新索引等级
    let index_level = calc_index_level(stargazing_index_today.total);
    observing_index_level.innerHTML = index_level[0];
    observing_index_level.classList.remove("default_index_level", "terrific", "average", "terrible");
    observing_index_level.classList.add(index_level[1]);
    today_index_level.innerHTML = index_level[0];
    today_index_level.classList.remove("default_index_level", "terrific", "average", "terrible");
    today_index_level.classList.add(index_level[1]);
    // 根据明日观星指数更新索引等级
    index_level = calc_index_level(stargazing_index_tomorrow.total);
    tomorrow_index_level.innerHTML = index_level[0];
    tomorrow_index_level.classList.remove("default_index_level", "terrific", "average", "terrible");
    tomorrow_index_level.classList.add(index_level[1]);
    // 根据后日观星指数更新索引等级
    index_level = calc_index_level(stargazing_index_two_days.total);
    two_days_index_level.innerHTML = index_level[0];
    two_days_index_level.classList.remove("default_index_level");
    two_days_index_level.classList.add(index_level[1]);
}

// TODO: 渲染
function render(params) {

    render_hourly_data(params).then(
        () => {
            // 渲染成功后, 更新未来24小时天气数据
            console.log("实时天气数据渲染成功");
        }
    );
    render_day_data(params).then(
        () => {
            // 渲染成功后, 更新日天气数据
            console.log("日天气数据渲染成功");
        }
    );
    render_light_pollution_data(params).then(
        () => {
            // 渲染成功后, 更新光害数据
            console.log("光害数据渲染成功");
        }
    );
    render_stargazing_index(params).then(
        () => {
            // 渲染成功后, 更新观星指数数据
            console.log("观星指数数据渲染成功");
        }
    );
}


// TODO: 初始化页面元素
async function init() {
    // 获取用户位置信息并渲染到页面上
    let data = await get_geolocation();
    // print(data.city)
    let en_city_name = data.city
    let city_data = await render_loc_data({city: en_city_name});
    print(city_data)
    print("初始化城市为: " )
    let params = {
        city: city_data.name
    }
    render(params)
}

init().then(
    () => {
        // 4. 绑定事件：点击搜索按钮
        search_icon.addEventListener('click', handle_search);

        // 5. 绑定事件：按回车键触发搜索
        city_input.addEventListener('keydown', (e) => {
            // 判断是否按的是Enter键（keyCode 13 或 key 'Enter'）
            if (e.key === 'Enter') {
                e.preventDefault(); // 阻止默认行为（如页面刷新）
                handle_search().then();
            }
        });
        console.log("页面初始化完成!");
    })

