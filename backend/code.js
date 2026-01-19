// --- CONFIGURATION ---
// Set these in Project Settings > Script Properties
// GITHUB_CLIENT_ID
// GITHUB_CLIENT_SECRET

function doGet(e) {
  const action = e.parameter.action;
  
  if (action === 'auth') {
    return exchangeCodeForToken(e.parameter.code);
  } else if (action === 'get_suggestions') {
    return getSuggestions(e);
  } else if (action === 'test_cors') {
     return jsonResponse({status: 'ok', method: 'GET'});
  }
  
  return ContentService.createTextOutput(JSON.stringify({status: 'error', message: 'Invalid action or method. Use POST for saving.'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  // Handle POST requests (Save Suggestion, Update Status)
  
  let data;
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return jsonResponse({status: 'error', message: 'Invalid JSON body'});
  }

  const action = e.parameter.action || data.action;

  if (action === 'save_suggestion') {
    return saveSuggestion(data);
  } else if (action === 'update_status') {
    return updateSuggestionStatus(data);
  }

  return jsonResponse({status: 'error', message: 'Unknown action: ' + action});
}

// --- AUTH FLOW ---

function exchangeCodeForToken(code) {
  const scriptProperties = PropertiesService.getScriptProperties();
  const client_id = scriptProperties.getProperty('GITHUB_CLIENT_ID');
  const client_secret = scriptProperties.getProperty('GITHUB_CLIENT_SECRET');
  
  if (!client_id || !client_secret) {
    return jsonResponse({error: 'Server misconfiguration: missing credentials'});
  }

  const payload = {
    client_id: client_id,
    client_secret: client_secret,
    code: code
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    headers: { Accept: 'application/json' },
    muteHttpExceptions: true
  };
  
  try {
    const response = UrlFetchApp.fetch('https://github.com/login/oauth/access_token', options);
    const data = JSON.parse(response.getContentText());
    return jsonResponse(data);
  } catch (err) {
    return jsonResponse({error: err.toString()});
  }
}

// --- SUGGESTION LOGIC ---

function saveSuggestion(data) {
  // Accepted Data Structure:
  // {
  //   user: { login: "...", email: "..." },
  //   meta: { realName: "...", comment: "..." },
  //   items: [ { type: "node", payload: {...} }, { type: "edge", payload: {...} } ]
  // }

  const sheet = getSheet();
  
  const id = Utilities.getUuid(); // Bundle ID
  const timestamp = new Date().toISOString();
  
  // Safe defaults
  const userLogin = data.user ? data.user.login : 'anonymous';
  const userEmail = data.user ? data.user.email : '';
  const realName = data.meta ? data.meta.realName : '';
  const generalComment = data.meta ? data.meta.comment : '';
  
  // We store the whole bundle as one row for simplicity, or we could split it.
  // Storing as one row is cleaner for "Review one suggestion block".
  
  sheet.appendRow([
    id, 
    timestamp, 
    userLogin, 
    userEmail, 
    'bundle', // Type is now bundle
    JSON.stringify(data.items), // Original payload is now items list
    'pending',
    realName,       // New Col 8
    generalComment  // New Col 9
  ]);
  
  return jsonResponse({status: 'success', id: id});
}


function getSuggestions(e) {
  // SECURITY CHECK
  const token = e.parameter.token;
  if (!token) {
     return jsonResponse({status: 'error', message: 'Missing access_token'});
  }
  
  if (!checkRepoWriteAccess(token)) {
     return jsonResponse({status: 'error', message: 'Access Denied: Read/Write permissions on repo required.'});
  }

  const sheet = getSheet();
  const rows = sheet.getDataRange().getValues();
  // Header is row 0
  
  const filterStatus = e.parameter.status || 'pending'; // Default pending
  const suggestions = [];
  
  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const currentStatus = row[6]; // Index 6 is Status

    // Logic: if filterStatus is 'all', take everything.
    // Otherwise match exact status.
    if (filterStatus === 'all' || currentStatus === filterStatus) {
      suggestions.push({
        id: row[0],
        timestamp: row[1],
        user: row[2],
        email: row[3],
        type: row[4],
        items: JSON.parse(row[5] || '[]'),
        status: row[6],
        realName: row[7] || '',
        comment: row[8] || '',
        processedBy: row[9] || '',   // New: Col 10
        processedAt: row[10] || ''   // New: Col 11
      });
    }
  }
  
  // Sort by timestamp desc (newest first)
  suggestions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  
  return jsonResponse({suggestions: suggestions});
}

function checkRepoWriteAccess(token) {
   try {
     const response = UrlFetchApp.fetch('https://api.github.com/repos/grafdedades/grafdedades.github.io', {
       headers: { 
         'Authorization': 'token ' + token,
         'Accept': 'application/vnd.github.v3+json'
       },
       muteHttpExceptions: true
     });
     
     if (response.getResponseCode() !== 200) return false;
     
     const data = JSON.parse(response.getContentText());
     // Check if user has push access
     if (data.permissions && data.permissions.push) {
       return true;
     }
     return false;
   } catch (e) {
     return false;
   }
}

function updateSuggestionStatus(data) {
  const sheet = getSheet();
  const rows = sheet.getDataRange().getValues();
  const processedBy = data.processedBy || 'admin';
  const processedAt = new Date().toISOString();
  
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] == data.id) {
      // Data Mapping:
      // Col 7 (Index 6) = Status
      // Col 10 (Index 9) = ProcessedBy
      // Col 11 (Index 10) = ProcessedAt
      
      sheet.getRange(i + 1, 7).setValue(data.status);
      sheet.getRange(i + 1, 10).setValue(processedBy);
      sheet.getRange(i + 1, 11).setValue(processedAt);
      
      return jsonResponse({status: 'updated'});
    }
  }
  
  return jsonResponse({status: 'error', message: 'ID not found'});
}

// --- HELPERS ---

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName('Suggestions');
  if (!sheet) {
    sheet = ss.insertSheet('Suggestions');
    // Header setup
    sheet.appendRow(['ID', 'Timestamp', 'GitHubUser', 'Email', 'Type', 'Payload/Items', 'Status', 'RealName', 'Comments', 'ProcessedBy', 'ProcessedAt']);
  } else {
    // Basic check to ensure headers exist if sheet was old
    // We can just rely on column indexing, but for clarity:
    // This part is lazily implicit.
    // The key is to ensure we read/write to correct index.
  }
  return sheet;
}

function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
