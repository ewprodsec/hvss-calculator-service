"use strict";

// Color constants for Rating highlighting
// ----------------------------------------
// BaseScoreColor
const COLOR_NONE = '#53aa33';
const COLOR_LOW = '#ffcb0d';
const COLOR_MEDIUM = '#f9a009';
const COLOR_HIGH = '#df3d03';
const COLOR_CRITICAL = '#cc0500';
const COLOR_DEFAULT = 'white';

const RANK_NONE = 'None';
const RANK_LOW = 'Low';
const RANK_MEDIUM = 'Medium';
const RANK_HIGH = 'High';
const RANK_CRITICAL = 'Critical';

// /#HVSS:1.0/AV:N/EAC:N/PR:N/UI:N/S:U/XIT:XCIA/C:N/I:N/A:N   (None)
// /#HVSS:1.0/AV:N/EAC:N/PR:N/UI:N/S:U/XIT:XCIA/C:N/I:L/A:H   (High)
// /#HVSS:1.0/AV:P/EAC:E/PR:H/UI:R/S:U/XIT:XCIA/C:L/I:L/A:L   (Low)
// /#HVSS:1.0/AV:A/EAC:L/PR:L/UI:R/S:U/XIT:XPS/XPS:L          (Low)
// /#HVSS:1.0/AV:A/EAC:L/PR:L/UI:R/S:U/XIT:XPS/XPS:MD         (Medium)
// /#HVSS:1.0/AV:P/EAC:L/PR:H/UI:R/S:U/XIT:XSD/XSD:SG         (Medium)
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:U/XIT:XHB/XHB:N          (None)
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:U/XIT:XHB/XHB:DA         (Medium)
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:U/XIT:XHB/XHB:NA         (Medium)
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XHB/XHB:NA         (High)
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XHB/XHB:UI         (Critical)

const vectorRegex = /^HVSS:1.0\/AV:[NALP]\/EAC:[ECHMLN]\/PR:[UNLH]\/UI:[NR]\/S:[UC]\/XIT:((XCIA\/C:[NLH]\/I:[NLH]\/A:[NLH])|(XPS\/XPS:([NLC]|MJ|MD))|(XSD\/XSD:(N|SL|PL|SG|PG))|(XHB\/XHB:(N|DA|NA|UI)))$/i;
// FIXME: replace 'const vectorRegex' with Hvss.vectorRegex

/*
  /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XCIA/C:N/I:N/A:L
  /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XPS/XPS:MD
  /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XSD/XSD:SG
  /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XHB/XHB:UI
*/
class VectorHvss10 extends Map {
  constructor() {
    super(vectorToMap('HVSS:1.0/AV:/EAC:/PR:/UI:/S:/XIT:/C:/I:/A:/XPS:/XSD:/XHB:'));
  }

  // constructor(vectorString) {
  //   const vs = (vectorString  !== undefined ) ? vectorString : 'HVSS:1.0/AV:/EAC:/PR:/UI:/S:/XIT:/C:/I:/A:/XPS:/XSD:/XHB:';
  //   super(vectorToMap(vs));
  // }

  /*
    Updates value only if key exists. Does not insert not predefined keys.
  */
  update(metric_name, metric_value) {
    if (this.has(metric_name)) {
      this.set(metric_name, metric_value);
    }
    return this;
  }

  getExpScopePart() {
    const full = mapToVector(this);
    return getExpScopePart(full); // Call Global function but not Class method (recursion)!
  }

  getCurrentXIT() {
    return this.get('XIT');
  }

  /*
    Examples:
      XIT:XCIA/C:N/I:N/A:L
      XIT:XPS/XPS:MD
      XIT:XSD/XSD:SG
      XIT:XHB/XHB:UI
  */
  getImpactPart(xit) {
    if (xit === undefined) {
      xit = this.getCurrentXIT(); // this.get(this.getCurrentXIT());
    }
    let xitMetricStr = '';
    if (xit === 'XCIA') {
      xitMetricStr = `C:${this.get('C')}/I:${this.get('I')}/A:${this.get('A')}`
    } else {
      xitMetricStr = `${xit}:${this.get(xit)}`
    }
    let xitString = `XIT:${xit}/${xitMetricStr}`;
    console.log(`--> DEBUG: getImpactPart(xit): ${xitString}`);
    return xitString;
  }

  vectorToString(xit) {
    return this.getExpScopePart() + this.getImpactPart(xit);
  }

}

const vectorCacheMap = new VectorHvss10();


// case 'None': return '#DAF7A6'; // #DAF7A6  // Nyanza #ECFFDC // Light Green	#90EE90
// case 'Low': return '#FFFAA0';       // Pastel Yellow	#FFFAA0
// case 'Medium': return '#FBCEB1';           // Apricot #FBCEB1  // Desert	#FAD5A5  // Peach #FFE5B4
// case 'High': return '#FAC898';      // Pastel Orange #FAC898
// case 'Critical': return '#F8C8DC';  // Pastel Pink #F8C8DC
// default: return 'white';

function setExploitability(baseExploitability) {
  const exploitability = document.getElementById('exploitability_subscore');
  exploitability.textContent = baseExploitability.toFixed(1);
}

function getCVSSExploitability(exploitability) {
  let cvssExp = exploitability * 0.39;
  if (cvssExp < 0.1) cvssExp = 0.1;
  return cvssExp;
}

function setNormalizedExploitability(exploitability) {
  const cvssExp = getCVSSExploitability(exploitability);
  document.getElementById('cvss_exploitability_subscore').textContent = cvssExp.toFixed(1);
}


/*
getRating() {
    const baseScore = this.getBaseScore();
    if (baseScore === 0) return RANK_NONE;
    else getExploitabilityRank(expScore);
}

getRating() {
    const baseScore = this.getBaseScore();
    if (baseScore === 0) return 'None';
    else if (baseScore < 4.0) return 'Low';
    else if (baseScore < 7.0) return 'Medium';
    else if (baseScore < 9.0) return 'High';
    else return 'Critical';
}

*/

function getExploitabilityRank(expScore) {
  if (expScore < 4.0) return RANK_LOW;
  else if (expScore < 7.0) return RANK_MEDIUM;
  else if (expScore < 9.0) return RANK_HIGH;
  else return RANK_CRITICAL;
}

function getColorByRating(rating) {
  switch (rating) {
    case RANK_NONE: return COLOR_NONE;
    case RANK_LOW: return COLOR_LOW;
    case RANK_MEDIUM: return COLOR_MEDIUM;
    case RANK_HIGH: return COLOR_HIGH;
    case RANK_CRITICAL: return COLOR_CRITICAL;
    default: return COLOR_DEFAULT;
  }
}

function setExploitabilityRankPanel(expRank) {
  document.getElementById('exploitability_rank').textContent = expRank;
  document.getElementById('expRankPanel').style.backgroundColor = getColorByRating(expRank);
}

function setBaseScore(result) {
  const xitCode = result.impactTypeCode.toLowerCase();
  const tdBaseId = `td_base_${xitCode}`;
  console.log(`--> DEBUG: tdBaseId=${tdBaseId}`);
  const e = document.getElementById(tdBaseId);
  e.innerHTML = `${result.base}<br>(${result.rating})`;
  e.style.color = COLOR_DEFAULT;
  e.style.backgroundColor = getColorByRating(result.rating);
}

function setImpactScore(result) {
  const xitCode = result.impactTypeCode.toLowerCase();
  const tdImpactId = `td_impact_${xitCode}`;
  console.log(`--> DEBUG: tdImpactId ${tdImpactId}`);
  // Negative Impact Subscore: -0.22 when Scope is Changed and ISS=0, it's Vector String = .../S:C/C:N/I:N/A:N
  const baseImpact = result.impactScore > 0 ? result.impactScore : 0.0;
  // document.getElementById(tdImpactId).textContent = baseImpact;
  const e = document.getElementById(tdImpactId);
  e.textContent = baseImpact;
}

// Global cache for Exploitability/Scope part of the vector
let currentExpScopePart = '';

// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XCIA/C:N/I:N/A:L
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XPS/XPS:MD
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XSD/XSD:SG
// /#HVSS:1.0/AV:A/EAC:N/PR:L/UI:N/S:C/XIT:XHB/XHB:UI

// /#HVSS:1.0/AV:P/EAC:N/PR:L/UI:N/S:C/XIT:XCIA/C:N/I:N/A:L

/*
  Find Exploitability/Scope part of the vector, e.g. HVSS:1.0/AV:A/EAC:N/PR:H/UI:N/S:C/
*/
function getExpScopePart(vectorString) {
  const xitIndex = vectorString.indexOf('XIT');
  const expScopePart = vectorString.substring(0, xitIndex);
  console.log(`--> DEBUG: expScopePart: ${expScopePart}`);
  return expScopePart;
}

function isExpScopeChanged(vectorString) {
  const expScopePart = getExpScopePart(vectorString);
  const isCanged = currentExpScopePart !== expScopePart;
  if (isCanged) currentExpScopePart = expScopePart;
  return isCanged;
}

function cleanupScorePanel() {
  document.querySelectorAll('#scoreTable tbody td:not(:first-child)')
    .forEach(cell => {
      cell.textContent = '';
      cell.style.backgroundColor = COLOR_DEFAULT;
    });
}

function cleanupErrorMessage() {
  // Clean up Error Message if it's not empty and visible
  const err = document.getElementById('errorMessage')
  if (err.style.visibility == 'visible') {
        err.textContent = ''
        err.style.visibility = 'hidden';
    }
}

function updateScorePanel(result) {
  setBaseScore(result);
  setExploitability(result.exploitability);
  // FIXME: CVSS-compatible Exploitability
  setNormalizedExploitability(result.exploitability);
  const expRank = getExploitabilityRank(result.exploitability);
  setExploitabilityRankPanel(expRank);

  setImpactScore(result);
}

function calculate(hvssVector) {
    console.log("calling backend with 'hvssVector' string: ", hvssVector);
    let hvssResult =  {success: false}
    $.ajaxSetup( { "async": false } );
    $.getJSON('/score', {vector: hvssVector }, function (data, textStatus, jqXHR) {
        console.log("Received response: ", JSON.stringify(data, null, 2));
        hvssResult = data;
    })
    .done(function () {
        hvssResult.success = true;
        console.log('Request successfully completed!'); })
    .fail(function (jqxhr,settings,ex) {
        console.log('Request failed: '+ ex); });
    console.log(`--> DEBUG: calculate(hvssVector) Result:\n${ JSON.stringify(hvssResult, null, 2) }`);
  return hvssResult;
}

function publishResult(result) {
  if (result.success === !0) {
    var L = document.querySelectorAll(".needBaseMetrics"), i = L.length;
    while (i--) { hide(L[i]) }
    parentNode(text("#baseMetricScore", result.base), '.scoreRating').className = 'scoreRating ' + result.rating.toLowerCase();
    text("#baseSeverity", "(" + result.rating + ")");
    show(inputValue("#vectorString", result.vector));

    // window.location.hash = result.vector;           <<<<---------------- TODO:--- FIXME:--- TODO:--- FIXME:--- TODO:

    // update custom score panel
    updateScorePanel(result);
  } else if (result.error === "Not all base metrics were given - cannot calculate scores.") {
    var L = document.querySelectorAll(".needBaseMetrics"), i = L.length;
    while (i--) { show(L[i]) }
    hide("#vectorString")
  }
}

function calculateAndPublish(vectorString) {
  cleanupErrorMessage();
  var result = calculate(vectorString);
  if (result.errorMessage) {
    const err = document.getElementById('errorMessage')
    err.textContent = 'Error: ' + result.errorMessage;
    err.style.visibility = "visible";
  } else {
    publishResult(result);
  }
}

function recalculateAll(vectorString) {
  // FIXME: FOR EACH XIT DO:                                 <<<<---------------- TODO:--- FIXME:--- TODO:--- FIXME:--- TODO:
  // vectorString = currentExpScopePart + currentXIT[TYPE]
  calculateAndPublish(vectorString);
}

function updateScores(vectorString) {
  vectorString = vectorString.toUpperCase();

  const test = vectorRegex.test(vectorString);
  console.log(`--> DEBUG: updateScores(vectorString) vectorRegex.test(vectorString) TEST: ${test}`);
  if (!test) {
    return;
  }

  // const map = vectorToMap(vectorString); // <<<<---------------- TODO:--- FIXME:--- TODO:--- FIXME:--- TODO:
  // mapToVector(map);                       // <<<<---------------- TODO:--- FIXME:--- TODO:--- FIXME:--- TODO:

  if (isExpScopeChanged(vectorString)) {
    // Clean up whole Score Panel if Exploitability/Scope is changed.
    cleanupScorePanel();
    recalculateAll(vectorString);
  } else {
    calculateAndPublish(vectorString);
  }
}

function vectorToMap(vectorString) {
  const map = new Map();
  vectorString.split('/').forEach(kv => {
    const v = kv.split(':');
    map.set(v[0], v[1]);
  });
  console.log(`--> DEBUG: vectorToMap(): ${JSON.stringify([...map])}`);
  return map;
}

function mapToVector(map) {
  let vectorString = '';
  let d = false;
  map.forEach((value, key) => {
    vectorString += `${d ? '/' : ''}${key}:${value}`;
    d = true;
  })
  console.log(`--> DEBUG: mapToVector(): ${vectorString}`);
  return vectorString;
}

function geEventSourceAttr(e) {
  console.log(`--> DEBUG: Event ('click'): e.target=${e.target}; e.srcElement=${e.srcElement}`);
  const attr = (e.target || e.srcElement).attributes;
  const name = attr.name.value;
  const id = attr.id.value;
  const value = attr.value.value;
  console.log(`--> DEBUG: Event Source Attributes: name=${name}; id=${id}; value=${value}`);
  /* it represents input attributes, e.g. <input name="XPS" value="MJ" id="XPS_MJ" type="radio"></input> */
  const attributes = new Map()
    .set('name', name)
    .set('id', id)
    .set('value', value);
  return attributes;
}

/*
  Update Current Vectors cache Map with provided metric and return new Vector Srting representation.
*/
function updateCurrentVector(metric_name, metric_value) {
  console.log(`--> DEBUG: updateCurrentVector() received "metric_name:metric_value" is: ${metric_name}:${metric_value}`);
  vectorCacheMap.update(metric_name, metric_value);
  const vectorString = vectorCacheMap.vectorToString();
  console.log(`--> DEBUG: updateCurrentVector() updated Vector Srting : ${vectorString}`);
  return vectorString;
}

function adjustXHB() {
  const none = document.getElementById('XHB_N');
  if (none.checked) return 'N';
  else if (document.getElementById('XHB_UI').checked) return 'UI';
  else if (document.getElementById('XHB_NA').checked) return 'NA';
  else if (document.getElementById('XHB_DA').checked) return 'DA';
  else {
    none.click();
    return 'N';
  }
}

function updateScoresOnInput(e) {
  const attr = geEventSourceAttr(e);
  const metric_name = attr.get('name');
  let metric_value = attr.get('value');
  if (metric_name === 'XHB') {
    metric_value = adjustXHB();
  }
  const vectorString = updateCurrentVector(metric_name, metric_value);
  updateScores(vectorString);
}


window.Element&&function(ElementPrototype){ElementPrototype.matchesSelector=ElementPrototype.matchesSelector||ElementPrototype.mozMatchesSelector||ElementPrototype.msMatchesSelector||ElementPrototype.oMatchesSelector||ElementPrototype.webkitMatchesSelector||function(selector){var node=this,nodes=(node.parentNode||node.document).querySelectorAll(selector),i=-1;while(nodes[++i]&&nodes[i]!=node);return!!nodes[i]}}(Element.prototype);var matchesSelector=function(node,selector){if(!('parentNode' in node)||!node.parentNode)return!1;return Array.prototype.indexOf.call(node.parentNode.querySelectorAll(selector))!=-1};function node(){for(var i=0;i<arguments.length;i++){var o=arguments[i];if(typeof(o)=='string'&&o)return document.querySelector(o);else if('nodeName' in o)return o;else if('jquery' in o)return o.get(0)}
return!1}

function parentNode(p,q){if(!p||!(p=node(p)))return;else if((typeof(q)=='string'&&p.matchesSelector(q))||p==q)return p;else if(p.nodeName.toLowerCase()!='html')return parentNode(p.parentNode,q);else return}

function bind(q,tg,fn){var o=node(q);if(!o)return;if(o.addEventListener){o.addEventListener(tg,fn,!1)}else if(o.attachEvent){o.attachEvent('on'+tg,fn)}else{o['on'+tg]=fn}
return o}

function text(q,s){
  var e=node(q);if(!e)return;
  if(arguments.length>1){
    if('textContent' in e){e.textContent=s}
    else{e.innerText=s}
    return e
  }
  return e.textContent||e.innerText
}

function hide(q){
  var e=node(q);
  if(!e)
    return;
  e.setAttribute('style','display:none');
  return e
}

function show(q){var e=node(q);if(!e)return;e.setAttribute('style','display:inline-block');return e}

function inputValue(q, v) {
  var e = document.querySelector(q);
  if (!e || e.nodeName.toLowerCase() != 'input')
    return;
  if (arguments.length > 1) {
    e.value = v;
    return e
  }
  return e.value
}

function setMetricsFromVector(vectorString) {
  var result = !0;
  var urlMetric;
  var metricValuesToSet = {};

  // const vectorRegex = /^HVSS:1.0\/AV:[NALP]\/EAC:[ECHMLN]\/PR:[UNLH]\/UI:[NR]\/S:[UC]\/XIT:((XCIA\/C:[NLH]\/I:[NLH]\/A:[NLH])|(XPS\/XPS:([NLC]|MJ|MD))|(XSD\/XSD:(N|SL|PL|SG|PG))|(XHB\/XHB:(N|DA|NA|UI)))$/i;
  // // FIXME: replace 'const vectorRegex' with Hvss.vectorRegex

  const test = vectorRegex.test(vectorString);
  console.log(`--> DEBUG: vectorString TEST: ${test}`);
  if (test) {
    var urlMetrics = vectorString.substring("HVSS:1.0/".length).split("/");
    for (var p in urlMetrics) {
      var urlMetric = urlMetrics[p].split(":");
      metricValuesToSet[urlMetric[0]] = urlMetric[1]
    }
    console.log(`--> DEBUG: metricValuesToSet: ${JSON.stringify(metricValuesToSet, null, '\t') }`);

    if (metricValuesToSet.AV !== undefined && metricValuesToSet.EAC !== undefined && metricValuesToSet.PR !== undefined && metricValuehvssVectorInURLsToSet.UI !== undefined && metricValuesToSet.S !== undefined
        && metricValuesToSet.XIT !== undefined
        && ((metricValuesToSet.C !== undefined && metricValuesToSet.I !== undefined && metricValuesToSet.A !== undefined)
            || metricValuesToSet.XPS !== undefined
            || metricValuesToSet.XSD !== undefined
            || metricValuesToSet.XHB !== undefined)) {
      for (var p in metricValuesToSet) {
        const eID = p + "_" + metricValuesToSet[p];
        console.log(`--> DEBUG: metricValuesToSet element ID: ${eID}`);
        const e = document.getElementById(eID);
        e.checked = true;
        if (p == 'XIT') e.click();
      }
      //
      // vectorCacheMap = new VectorHvss10(vectorString);
      // updateScores(vectorString);

    } else { result = "NotAllBaseMetricsProvided" }
  } else { result = "MalformedVectorString" }
  console.log(`--> DEBUG: result: ${result}`);

  // vectorCacheMap = new VectorHvss10(vectorString);
  updateScores(vectorString);
  return result;
}

var hvssVectorInURL;

function urlhash() {
  var h = window.location.hash;
  hvssVectorInURL = h;
  console.log(`urlhash(): '${h}'`);
  setMetricsFromVector(h.substring(1));
}

// function inputSelect(){
//   this.setSelectionRange(0,this.value.length)
// }

//  export { Hvss, HvssBaseResult, ImpactTypes, ValidationError, metric_hvss10, factors_config };

function hvssCalculator() {
  console.log(`--> DEBUG: hvss-calc_helptext.js - HVSS10_Help..XPS_C_Label=${HVSS10_Help.helpText_en.XPS_C_Label}`);

  var L, i, n;
  L = document.querySelectorAll('.cvss-calculator input'); // input:not(.tablink)

  i = L.length;
  while (i--) {
    bind(L[i], 'click', updateScoresOnInput);
  }
  for (n in HVSS10_Help.helpText_en) {
    // console.log(`--> DEBUG: n: ${n}`);
    document.getElementById(n).setAttribute('title', HVSS10_Help.helpText_en[n])
  }
  urlhash();
  if (("onhashchange" in window)) { window.onhashchange = urlhash }
  // bind(bind("#vectorString", 'click', inputSelect), "contextmenu", inputSelect)
};

hvssCalculator();
