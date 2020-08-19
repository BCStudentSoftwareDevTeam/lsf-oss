valueTI = ["tabindex=2", "tabindex=3", "tabindex=4", "tabindex=5", "tabindex=6", "tabindex=7", "tabindex=8", "tabindex=9", "tabindex=10", "tabindex=11", "tabindex=12", "tabindex=13"]
valueTitle = ["students", "dept", "lsf", "admin", "pending", "overload", "past", "manageT", "manageD", "manageA", "email", "logout"]

function checkBrowser() {
  // Get the user-agent string
  let userAgentString = navigator.userAgent;

  // Detect Chrome
  let chromeAgent = userAgentString.indexOf("Chrome") > -1;

  if (chromeAgent = true) {
    varTabIndex = "tabindex=0"
  } else {
    varTabIndex =
  }


  //document.querySelector(".output-chrome").textContent = chromeAgent;
