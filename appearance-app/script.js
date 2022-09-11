function searchBirds(display) { // Find birds in birdsLibrary that match user's criteria and display them if Boolean parameter display is true; else, return list possibleBirds; 3C Segment 1 - includes sequencing (steps are in order), selection (there are if-statements), and iteration (it checks all birds in birdsLibrary to see if they match criteria)
  var name = document.getElementById('nameInput').value; // String name of bird user saw (or '', if they didn't input name)
  var size = document.getElementById('sizeSelect').value; // String size of bird user saw (or '', if they didn't input size)
  var colors = []; // Array of string colors of bird user saw (or [], if they didn't input colors); init empty array
  var colorsSelect = document.getElementById('colorsSelect').options;
  for (var i=0; i<colorsSelect.length; i++) { // Iteration
    if(colorsSelect[i].selected) { // Selection
      colors.push(colorsSelect[i].value); // Append to colors the colors in <colorsSelect> that user selected
    }
  }
  if (name) { // If user inputted a name; selection
    for (var i=0; i<Object.keys(birdsLibrary).length; i++) { // Go through all birds in birdsLibrary; iteration
      if(name.toLowerCase() == eval('birdsLibrary.bird' + i + '.name').toLowerCase()) { // If name of bird at i in birdsLibrary matches name of bird user saw; selection
        if (display) { // Selection
          clearDiv('output');
          displayBird(i); // Display that bird
          return; // Stop searchBirds()
        }
      }
    }
  }
  var possibleBirds = []; // If user didn't find bird by name, init possibleBirds as empty array; will hold the integer i (for 'bird9', i=9) for birds in birdsLibrary that match user's inputted size or color
  if (size) { // If user inputted a size; selection
    for (var i=0; i<Object.keys(birdsLibrary).length; i++) { // Go through all birds in birdsLibrary; iteration
      if(size == eval('birdsLibrary.bird' + i + '.size')) { // If size of bird at i in birdsLibrary matches size of bird user saw; selection
        possibleBirds.push(i); // Append i to possibleBirds
      }
    }
  }
  if (colors) { // If user inputted colors; selection
    for (var i=0; i<Object.keys(birdsLibrary).length; i++) { // Go through all birds in birdsLibrary; iteration
      if (colors.sort().join('') == eval('birdsLibrary.bird' + i + '.colors').sort().join('')) { // If colors of bird at i in birdsLibrary perfectly matches colors of bird user saw; selection
        possibleBirds.push(i); // Append i to possibleBirds
      }
    }
  }
  possibleBirds = possibleBirds.filter(onlyUnique); // Remove duplicates from possibleBirds
  if (display) { // If Boolean parameter display is true; selection
    clearDiv('output'); // Clear #output <div> before displaying birds
    possibleBirds.forEach(function(i) { // Display all possibleBirds
      displayBird(i);
    });
  } else {
    if (possibleBirds.length == 0) { // If possibleBirds is empty, fill it with all i for birds in birdsLibrary; selection
      for (var i=0; i<Object.keys(birdsLibrary).length; i++) { // Iteration
        possibleBirds.push(i);
      }
    }
    return possibleBirds; // Else, return possibleBirds (don't display them)
  }
}

function displayBird(i) { // Given integer parameter i associated with bird, dispaly it as #container with #image, #overlay with description, #saveLifeBtn, and #saveWishBtn to allow user to save bird in lifeList or wishList (using information for bird at i in birdsLibrary)
  var bird = eval('birdsLibrary.bird' + i); // Get bird object at i from birdsLibrary
  var container = myCreateElement('DIV', 'container', null, 'output', null); // Create #container <div>, inside will be
  var image = myCreateElement('IMG', 'image', null, null, container); // #image of bird
  image.src = bird.imageLink;
  var overlay = myCreateElement('P', 'overlay', null, null, container); // #overlay with information about bird
  overlay.innerHTML = '<b>' + bird.name + '</b>: ' + bird.size + ' ' + displayArr(bird.colors); // Get information about bird (from birdsLibrary)
  var saveLifeBtn = myCreateElement('BUTTON', ('saveLifeBtn' + i), 'saveLifeBtn', null, container); // .saveLifeBtn that allows user to save bird to lifeList
  saveLifeBtn.innerHTML = '🌟';
  saveLifeBtn.onclick = function() { saveBird(i, lifeList); };
  var saveWishBtn = myCreateElement('BUTTON', ('saveWishBtn' + i), 'saveWishBtn', null, container); // .saveWishBtn that allows user to save bird to wishList
  saveWishBtn.innerHTML = '🔖';
  saveWishBtn.onclick = function() { saveBird(i, wishList); };
  if (lifeList.includes(i)) { // If the bird being displayed has already been saved in lifeList
    saveLifeBtn.style.backgroundColor = '#52B788'; // Change background-color of #saveLifeBtn to green (represents that user has seen this bird)
  }
  if (wishList.includes(i)) { // If the bird being displayed has already been saved in wishList
    saveWishBtn.style.backgroundColor = '#52B788'; // Change background-color of #saveWishBtn to green (represents that user wishes to see this bird)
  }

}

function displayAllBirds() { // Display all birds in birdsLibrary
  clearDiv('output');
  for (var i=0; i<Object.keys(birdsLibrary).length; i++) { // Go through all birds in birdsLibrary
    displayBird(i); // Display bird
  }
}

function displayRandomBird(completelyRandom) { // Display random bird depending on Boolean parameter completelyRandom: if completelyRandom is true, display completely random bird in birdsLibrary; else, display random bird that matches user's criteria
  clearDiv('output');
  if (completelyRandom) {
    displayBird(randomInteger(0, (Object.keys(birdsLibrary).length-1))); // Generate random number in range of how many birds are in birdsLibrary; display bird at that completely random number
  } else { // 3C Segment 2 - 3D function call 2
    var possibleBirds = searchBirds(false); // Get array of i for birds that match user's criteria
    displayBird(possibleBirds[randomInteger(0, (possibleBirds.length-1))]); // Generate random index in range of how many birds in possibleBirds; get i of possibleBird at that index; display bird at i
  }
}

function saveBird(i, myBirds) { // If user presses .saveBtn, save integer parameter i associated with that bird to list parameter myBirds (either lifeList or wishList); 3B Segment 1
  if (myBirds.indexOf(i) == -1) { // If bird at i isn't already in myBirds, change .saveBtn color aptly and save it to myBirds
    document.getElementById('save' + (myBirds == lifeList ? 'Life' : 'Wish') + 'Btn' + i).style.backgroundColor = '#52B788'; // Change background-color of #saveLifeBtn to green (represents that user saved this bird)
    myBirds.push(i); // Append i to myBirds to save it
  } else { // Else, bird at i already in myBirds, change .saveBtn color aptly and remove it from myBirds
    document.getElementById('save' + (myBirds == lifeList ? 'Life' : 'Wish') + 'Btn' + i).style.backgroundColor = '#2D6A4F'; // Change background-color of #saveBtn to dark green (represents that user hasn't saved this bird)
    myBirds.splice(myBirds.indexOf(i), 1); // Remove i from myBirds
  }
}

function displayMyBirds(myBirds) { // Display all birds user saved in list parameter myBirds (either lifeList or wishList); 3B Segment 2
  clearDiv('output');
  myBirds.forEach(function(i) { // Get each i associated with saved birds
    displayBird(i); // Display bird
  });
}

function myCreateElement(elType, myId, myClass, parentDivId, parentDiv) { // Create element el of elType (string parameter type of element) with myId and myClass (string parameters of HTML ID and className), append it to parentDivId/parentDiv (string parameter of id of parent <div> or JS variable parameter of HTML <div> object), and return el (so other properties can be added to el)
  var el = document.createElement(elType);
  if (myId) {
    el.id = myId;
  }
  if (myClass) {
    el.className = myClass;
  }
  if (parentDivId) {
    document.getElementById(parentDivId).appendChild(el);
  } else if (parentDiv) {
    parentDiv.appendChild(el);
  }
  return el;
}

function clearDiv(divID) { // Given string parameter divID, clear the <div> with that ID (given that it exists)
  var divEl = document.getElementById(divID);
  if (divEl) {
    divEl.innerHTML = '';
  }
}

function randomInteger(min, max) { // Return random integer between integer parameters min and max (inclusive); attribution to https://www.w3schools.com/js/js_random.asp
  return Math.floor(Math.random() * (max+1)) + min;
}

function onlyUnique(value, index, self) { // Return arr of unique values (no duplicates); attribution to https://stackoverflow.com/questions/1960473/get-all-unique-values-in-a-javascript-array-remove-duplicates
  return self.indexOf(value) === index;
}

function displayArr(arr) { // Displays list parameter arr with apt ',' 'and' '.' as a return string str
  var str = '';
  for(var i=0; i<arr.length; i++) {
    if (i == arr.length-2) {
      str += arr[i] + ', and '
    } else if (i == arr.length-1) {
      str += arr[i] + '.'
    } else {
      str += arr[i] + ', '
    }
  }
  return str;
}

var lifeList = []; // Array of integers i associated with birds user has seen; 3B Segment 1

var wishList = []; // Array of integers i associated with birds user wishes to see

var birdsLibrary = { // Object with sub-objects for each bird; birds are identified by integer i (for 'bird9', i=9)
  bird0: { // In each bird sub-object, have properties store
    name: 'Canada Goose', // Sring of bird name
    size: 'large', // String of bird size
    colors: ['brown', 'black', 'white'], // Array with strings of bird's colors
    imageLink: 'https://upload.wikimedia.org/wikipedia/commons/4/40/Canada_goose_on_Seedskadee_NWR_%2827826185489%29.jpg' // String that holds image adress to an image of that bird
  },
  bird1: {
    name: 'Mallard',
    size: 'medium',
    colors: ['brown', 'black', 'white', 'green', 'blue'],
    imageLink: 'https://upload.wikimedia.org/wikipedia/commons/b/bf/Anas_platyrhynchos_male_female_quadrat.jpg'
  },
  bird2: {
    name: 'Mute Swan',
    size: 'large',
    colors: ['white'],
    imageLink: 'https://upload.wikimedia.org/wikipedia/commons/3/35/Mute_swan_Vrhnika.jpg'
  },
  bird3: {
    name: 'Herring Gull',
    size: 'medium',
    colors: ['white', 'grey'],
    imageLink: 'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/303381091/1800'
  },
  bird4: {
    name: 'Wild Turkey',
    size: 'large',
    colors: ['brown', 'black'],
    imageLink: 'https://www.thespruce.com/thmb/kx1_j5yiGp71z5HGcpQD5MatfWQ=/3395x2546/smart/filters:no_upscale()/wild-turkey-560606673-57d81e6e5f9b589b0a98254f.jpg'
  },
  bird5: {
    name: 'Rock Pigeon',
    size: 'medium',
    colors: ['grey', 'white'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/308065631-480px.jpg'
  },
  bird6: {
    name: 'Red-Tailed Hawk',
    size: 'large',
    colors: ['brown', 'white', 'red'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/60384911-480px.jpg'
  },
  bird7: {
    name: 'Turkey Vulture',
    size: 'large',
    colors: ['black', 'brown'],
    imageLink: 'https://bloximages.chicago2.vip.townnews.com/montrosepress.com/content/tncms/assets/v3/editorial/d/1b/d1b8d314-c2e3-11ea-bf1a-2f104baa9617/5f08c1ef0be37.image.jpg'
  },
  bird8: {
    name: 'Bald Eagle',
    size: 'large',
    colors: ['brown', 'white'],
    imageLink: 'https://www.adirondackalmanack.com/wp-content/uploads/2020/05/eagle_ninilchka_5.jpg'
  },
  bird9: {
    name: 'Great Horned Owl',
    size: 'medium',
    colors: ['brown'],
    imageLink: 'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/297363481/1800'
  },
  bird10: {
    name: 'Red-Bellied Woodpecker',
    size: 'small',
    colors: ['black', 'white', 'red'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/64995071-480px.jpg'
  },
  bird11: {
    name: 'Blue Jay',
    size: 'small',
    colors: ['blue', 'white'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/59859171-480px.jpg'
  },
  bird12: {
    name: 'American Crow',
    size: 'medium',
    colors: ['black'],
    imageLink: 'https://www.allaboutbirds.org/guide/noindex/photo/70580311-480px.jpg'
  },
  bird13: {
    name: 'American Robin',
    size: 'small',
    colors: ['brown', 'red'],
    imageLink: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Turdus-migratorius-002.jpg/1200px-Turdus-migratorius-002.jpg'
  },
  bird14: {
    name: 'Eastern Bluebird',
    size: 'small',
    colors: ['blue', 'orange', 'white'],
    imageLink: 'https://www.almanac.com/sites/default/files/styles/primary_image_in_article/public/image_nodes/bluebird-3456115_1920.jpg?itok=LL0Zpqxg'
  },
  bird15: {
    name: 'Black-Capped Chickadee',
    size: 'small',
    colors: ['grey', 'white', 'black'],
    imageLink: 'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/302473191/1800'
  },
  bird16: {
    name: 'Tufted Titmouse',
    size: 'small',
    colors: ['grey', 'white'],
    imageLink: 'https://cdn.britannica.com/78/39878-050-C5E51F47/range-tufted-titmouse-portion-half.jpg'
  },
  bird17: {
    name: 'Song Sparrow',
    size: 'small',
    colors: ['brown'],
    imageLink: 'https://static.scientificamerican.com/blogs/cache/file/CF131687-8C9A-4FAD-982B239120D74750_source.jpg?w=590&h=800&901C7AF1-049F-4C9D-B6F1EDF4E945141A'
  },
  bird18: {
    name: 'House Sparrow',
    size: 'small',
    colors: ['brown'],
    imageLink: 'https://nas-national-prod.s3.amazonaws.com/styles/hero_cover_bird_page/s3/house-sparrow_001_winter_poland_hederabaltica_flickrccby-sa-2.0_adult-male.jpg?itok=nY4joGAo'
  },
  bird19: {
    name: 'House Finch',
    size: 'small',
    colors: ['red', 'grey'],
    imageLink: 'https://ca-times.brightspotcdn.com/dims4/default/72a4efc/2147483647/strip/true/crop/2048x1152+0+0/resize/1486x836!/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Ffe%2F65%2F052a5bb882397b74a62b3fe5e4c5%2Fsd-1526586990-uuv2boke0o-snap-image'
  },
  bird20: {
    name: 'Northern Cardinal',
    size: 'medium',
    colors: ['red'],
    imageLink: 'https://www.thespruce.com/thmb/P2D57NIaR6WLK5W2EbpTk8JzsBQ=/1500x1000/filters:fill(auto,1)/northern-cardinal-snow-5a76385f3128340036ab3a23.jpg'
  },
  bird21: {
    name: 'Brown-Headed Cowbird',
    size: 'medium',
    colors: ['black', 'brown'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/306622781-480px.jpg'
  },
  bird22: {
    name: 'Red-Winged Blackbird',
    size: 'medium',
    colors: ['black', 'red', 'yellow'],
    imageLink: 'https://www.thespruce.com/thmb/JMEH3XLgNKTagzrCILwgPvr8CJw=/2335x2335/smart/filters:no_upscale()/red-winged-blackbird-identification-385990-hero-bca4cabf8e9743e8b2459ce6421dc642.jpg'
  },
  bird23: {
    name: 'Belted Kingfisher',
    size: 'small',
    colors: ['blue', 'white', 'red'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/303715931-480px.jpg'
  },
  bird24: {
    name: 'Merlin',
    size: 'large',
    colors: ['grey', 'brown', 'white'],
    imageLink: 'https://www.allaboutbirds.org/guide/assets/photo/303425061-480px.jpg'
  }
}

// NOTE: attribution for images of birds goes to Wikipedia, Cornell Lab of Ornithology, and All-About-Birds
