/*
Template Name: Skote - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: job list Init Js File
*/

// var url = "/static/js/lia_projects/";
var url = "http://localhost:8000";
var allJobList = '';

var prevButton = document.getElementById('page-prev');
var nextButton = document.getElementById('page-next');

// configuration variables
var currentPage = 1;
var itemsPerPage = 8;

//Job list by json
var getJSON = function (jsonurl, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url + jsonurl, true);
    xhr.responseType = "json";
    xhr.onload = function () {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
};

// get json
getJSON("/lia_projects/api/view_list/", function (err, data) {

    if (err !== null) {
        console.log("Something went wrong: " + err);
    } else {
        allJobList = data;
        loadListData(allJobList, currentPage);
        paginationEvents();
    }
});


function loadListData(datas, page) {
    var pages = Math.ceil(datas.length / itemsPerPage)
    // make sure page is in bounds 
    if (page < 1) page = 1
    if (page > pages) page = pages
    document.querySelector("#projectgrid-list").innerHTML = '';

    for (var i = (page - 1) * itemsPerPage; i < (page * itemsPerPage) && i < datas.length; i++) {
        if (datas[i]) {
            console.log('datas', datas[i])
            var projectDetailsUrls = "/lia_projects/detail/" + datas[i].id;
            document.querySelector("#projectgrid-list").innerHTML += '<div class="col-xl-3 col-md-6">\
        <div class="card">\
            <div class="card-body  mb-0 pb-0">\
             <h5 class="fs-17 mb-2"><a href="javascript:void(0);" class="text-dark">' + datas[i].project_title + '</a></h5>\
               <hr>\
                </div>\
                   <div class="card">\
            <div class="card-body"> \
                <div class="table-responsive">\
                    <table class="table">\
                        <tbody> \
                        <tr>\
                                <th scope="row">Ente</th>\
                                <td>' + datas[i].company.name + '</td>\
                            </tr>\
                             <tr>\
                                <th scope="row">Sostenitore</th>\
                                <td>' + datas[i].supporters[0].name + '</td>\
                            </tr>\
                            <tr>\
                                <th scope="row">Partner Principale</th>\
                                <td>' + datas[i].lead_partner[0].name + '</td>\
                            </tr>\
                            <tr>\
                                <th scope="row">Partners</th>\
                                <td>' + datas[i].partner[0].name + '</td>\
                            </tr>\
                            <tr>\
                                <th scope="row">Aziende Utilzzatrici</th>\
                                <td>\
                <a href="#!" class="px-3 py-2 rounded bg-light bg-opacity-50 d-block mb-2">Azienda 1<span class="badge text-bg-info float-end bg-opacity-100">52</span></a>\
                <a href="#!" class="px-3 py-2 rounded bg-light bg-opacity-50 d-block mb-2">Azienda 2 <span class="badge text-bg-info float-end bg-opacity-100">10</span></a>\
                <a href="#!" class="px-3 py-2 rounded bg-light bg-opacity-50 d-block mb-2">Azienda 3 <span class="badge text-bg-info float-end bg-opacity-100">64</span></a>\
                <a href="#!" class="px-3 py-2 rounded bg-light bg-opacity-50 d-block mb-2">Azienda 4 <span class="badge text-bg-info float-end bg-opacity-100">105</span></a>\
                                </td>\
                            </tr>\
                        <tr>\
                                <th scope="row">Status</th>\
                                <td>' + datas[i].status + '</td>\
                            </tr>\
                            <tr>\
                                <th scope="row">Data inizio</th>\
                                <td>' + datas[i].start_date + '</td>\
                            </tr>\
                            <tr>\
                                <th scope="row">Data fine</th>\
                                <td>' + datas[i].end_date + '</td>\
                            </tr>\
                        </tbody>\
                    </table>\
                </div> \
                <div class="mt-4 hstack gap-2">\
                    <a href="' + projectDetailsUrls + '" target="_blank" class="btn btn-soft-success w-100">Dettaglio Progetto</a>\
                </div>\
            </div>\
            </div>\
        </div>\
       </div>\
    </div>';
        }
    }
    selectedPage();
    currentPage == 1 ? prevButton.classList.add('disabled') : prevButton.classList.remove('disabled');
    currentPage == pages ? nextButton.classList.add('disabled') : nextButton.classList.remove('disabled');
}


//datepicker1 filter
var date = new Date();
var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());

$('#datepicker1 input').datepicker('setDate', today).on('changeDate', function (e) {
    var pickerVal = document.querySelector("#datepicker1 input").value;
    var filterData = allJobList.filter(function (data) {
        return new Date(data.postDate) <= new Date(pickerVal)
    });

    var pageNumber = document.getElementById('page-num');
    pageNumber.innerHTML = "";
    var dataPageNum = Math.ceil(filterData.length / itemsPerPage)
    // for each page
    for (var i = 1; i < dataPageNum + 1; i++) {
        pageNumber.innerHTML += "<a class='page-link clickPageNumber' href='#'>" + i + "</a>";
    }

    loadListData(filterData, currentPage);
});
;

function selectedPage() {
    var pagenumLink = document.getElementById('page-num').getElementsByClassName('clickPageNumber');
    for (var i = 0; i < pagenumLink.length; i++) {
        if (i == currentPage - 1) {
            pagenumLink[i].classList.add("active");
        } else {
            pagenumLink[i].classList.remove("active");
        }
    }
};

// paginationEvents
function paginationEvents() {
    var numPages = function numPages() {
        return Math.ceil(allJobList.length / itemsPerPage);
    };

    function clickPage() {
        document.addEventListener('click', function (e) {
            if (e.target.nodeName == "A" && e.target.classList.contains("clickPageNumber")) {
                currentPage = e.target.textContent;
                loadListData(allJobList, currentPage);
            }
        });
    };

    function pageNumbers() {
        var pageNumber = document.getElementById('page-num');
        pageNumber.innerHTML = "";
        // for each page
        for (var i = 1; i < numPages() + 1; i++) {
            pageNumber.innerHTML += "<a class='page-link clickPageNumber' href='#'>" + i + "</a>";
        }
    }

    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            loadListData(allJobList, currentPage);
        }
    });

    nextButton.addEventListener('click', function () {
        if (currentPage < numPages()) {
            currentPage++;
            loadListData(allJobList, currentPage);
        }
    });

    pageNumbers();
    clickPage();
    selectedPage();
}

// Search list
var searchElementList = document.getElementById("searchProject");
searchElementList.addEventListener("keyup", function () {
    var inputVal = searchElementList.value.toLowerCase();

    function filterItems(arr, query) {
        return arr.filter(function (el) {
            return el.project_title.toLowerCase().indexOf(query.toLowerCase()) !== -1
        })
    }

    var filterData = filterItems(allJobList, inputVal);

    searchResult(filterData);
    loadListData(filterData, currentPage);
});


function searchResult(data) {
    if (data.length == 0) {
        document.getElementById("pagination-element").style.display = "none";
    } else {
        document.getElementById("pagination-element").style.display = "flex";
    }

    var pageNumber = document.getElementById('page-num');
    pageNumber.innerHTML = "";
    var dataPageNum = Math.ceil(data.length / itemsPerPage)
    // for each page
    for (var i = 1; i < dataPageNum + 1; i++) {
        pageNumber.innerHTML += "<div class='page-item'><a class='page-link clickPageNumber' href='javascript:void(0);'>" + i + "</a></div>";
    }
}