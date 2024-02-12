const form = document.getElementById('utmForm');
const resultDiv = document.getElementById('resultText');
let field1 = document.getElementById('id_base_url');
let field2 = document.getElementById('id_utm_source');
let field3 = document.getElementById('id_utm_medium');
let field4 = document.getElementById('id_utm_campaign');
let field5 = document.getElementById('id_utm_content');
let field6 = document.getElementById('id_utm_term');

function createUtmUrl() {
    let coloredField4 = '';
    let coloredField5 = '';
    let coloredField6 = '';


    let resultString;
    let params;
    let baseUrl;
    if (field1.value.includes('?')) {
        result = parseUTMParams(field1.value)
        baseUrl = result['baseUrl']
        params = result['utmParams']
        field1.value = baseUrl
        if (params !== null && params !== undefined) {
            
            if (params.hasOwnProperty('utm_source')) {                
                field2.value = params['utm_source'];
            }
            if (params.hasOwnProperty('utm_medium')) {            
                field3.value = params['utm_medium'];
            }
            if (params.hasOwnProperty('utm_campaign')) {            
                field4.value = params['utm_campaign'];
            }
            if (params.hasOwnProperty('utm_content')) {            
                field5.value = params['utm_content'];
            }
            if (params.hasOwnProperty('utm_term')) {            
                field6.value = params['utm_term'];
            }
        }
    }

    let coloredField2 = '<span class="text-blue-600">?utm_source=' + field2.value + '</span>';
    let coloredField3 = '<span class="text-lime-500">&utm_medium=' + field3.value + '</span>';
    if (field4.value) {
        coloredField4 = '<span class="text-red-600">&utm_campaign=' + field4.value + '</span>';
        }
    if (field5.value) {
        coloredField5 = '<span class="text-indigo-600">&utm_content=' + field5.value + '</span>';
        }
    if (field6.value) {
        coloredField6 = '<span class="text-amber-600">&utm_term=' + field6.value + '</span>';
        }


    resultString = field1.value + coloredField2 + coloredField3 + coloredField4 + coloredField5 + coloredField6;

    if (field1.value && field2.value && field3.value) {
        resultDiv.innerHTML = resultString;
        }

}

function parseUTMParams(url) {
    const [baseUrl, queryString] = url.split('?');
  
    if (!queryString) {
      return {};
    }
  
    const queryParams = queryString.split('&');
  
    const utmParams = {};
  
    queryParams.forEach(param => {
      const [key, value] = param.split('=');
      utmParams[key] = value;
    });
  
    return { baseUrl, utmParams };
  }

form.addEventListener('input', createUtmUrl);
field1.addEventListener('blur', function(){
    if (field1.value !== '') {
        if (!field1.value.match(/^https?:\/\//)) {
            field1.value = 'https://' + field1.value;
            createUtmUrl();
        }
    }
})

function copyToClipboard() {
    var resultElement = document.getElementById("resultText");

    var range = document.createRange();
    range.selectNode(resultElement);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);

    document.execCommand("copy");

    window.getSelection().removeAllRanges();
    const svgContainer = document.getElementById('icon-container').querySelector('svg');

    let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    newPath.setAttribute('d', 'M11 14l2 2l4 -4');
    svgContainer.appendChild(newPath);
  }


  let suggestions = document.getElementsByClassName('suggestion');

  for (let i = 0; i < suggestions.length; i++) {
      suggestions[i].addEventListener('click', function(e) {
          e.target.parentElement.previousElementSibling.lastElementChild.value = e.target.innerText;
          createUtmUrl();
      });
  }
