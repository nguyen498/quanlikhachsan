// let remaining in checkout.html
let customerContainer = document.getElementById('customer-container');
let btnAddCustomer = document.getElementById('btn-add-customer');
let btnDeleteCustomer = document.getElementById('btn-delete-customer');
let customerCounterNumber = document.getElementById('customer-counter-number');
let count = 0;
let familyMembersCounter = document.getElementById('family-members-counter');

let price = document.getElementById('price');
let dayOfStay = document.getElementById('date-of-stay');
let totalAmount = document.getElementById('total-amount');
let checkInTime = document.getElementById('checkInTime');
let checkOutTime = document.getElementById('checkOutTime');

function createCustomerBox(index = 0, customerName = '', customerType = {}, idCard = '', address = '') {
    const customerBox = document.createElement("div");
    customerBox.innerHTML = `
    <!-- Card -->
      <div id="checkout-form-${index}" class="card wish-list pb-1 mb-4">

        <div class="card-body">
          <a class="dark-grey-text d-flex justify-content-between collapsed" data-toggle="collapse"
            href="#customerCollapse-${index}" aria-expanded="false" aria-controls="customerCollapse-${index}">
            Khách Hàng ${index}
            <span id="btn-delete-customer" onclick="deleteCustomerBox('#checkout-form-${index}')" class="d-flex align-items-center badge badge-danger ml-auto mr-4">Delete</span>
            <span><i class="fas fa-chevron-down pt-1"></i></span>
          </a>
        
          <div class="collapse" id="customerCollapse-${index}" style="">
            <div class="mt-3">
              <!-- Customer Name -->
              <div class="md-form md-outline mb-0 mb-lg-4">
                <input type="text" id="customerName[]" name="customerName[]" value="${customerName}" class="form-control mb-0 mb-lg-2" required>
                <label for="customerName[]">Tên Khách Hàng *</label>
              </div>
              
              
              <!-- Customer Type  -->
              <div class="md-form md-outline mb-0 mb-lg-4">
                <select name="customerType[]" class="browser-default custom-select" required>
                  <option value="" selected>Chọn Loại Khách *</option>
                  {% for customerTypedb in customer_types_db %}
                  <option value="{{customerTypedb.id}}">{{customerTypedb.name}}</option>
                  {% endfor %}
                </select>
              </div>

              <!-- Id  -->
              <div class="md-form md-outline mb-0 mb-lg-4">
                <input type="text" id="idCard[]" name="idCard[]" value="${idCard}" inputmode="numeric" pattern="[0-9\s]{8,12}" class="form-control mb-0 mb-lg-2">
                <label for="idCard[]">CMND / CCCD (8 đến 12 số) (Bỏ trống CMND nếu không có)</label>
              </div>
              
              <!-- address  -->
              <div class="md-form md-outline mb-0 mb-lg-4">
                <input type="text" id="address[]" name="address[]" value="${address}" class="form-control mb-0 mb-lg-2" required>
                <label for="address[]">Địa Chỉ *</label>
              </div>
            </div>
          </div>
        </div>

      </div>
    <!-- Card -->
    `;
    return customerBox;
};

function addCustomerBox() {
    if (remaining > 0) {
        parseInt(familyMembersCounter.innerText++);
        count++;
        remaining--;
        customerContainer.appendChild(createCustomerBox(count));
        updateCounterUI();
    }
};

function deleteCustomerBox($target) {
    if (confirm("Are you sure you want to delete this customer?")) {
        document.querySelector($target).remove();
        parseInt(familyMembersCounter.innerText--);
        remaining++;
        updateCounterUI();
    }
};

function updateCounterUI() {
    customerCounterNumber.innerHTML = remaining;
};


var DateDiff = {
    inDays: function (d1, d2) {
        var t2 = d2.getTime();
        var t1 = d1.getTime();

        return Math.floor((t2 - t1) / (24 * 3600 * 1000));
    }
};

function getCheckValue() {
    let d1 = new Date(checkInTime.value);
    let d2 = new Date(checkOutTime.value);
    let totalDay = DateDiff.inDays(d1, d2);

    if (!isNaN(d1) && !isNaN(d2)) {
        dayOfStay.innerText = (totalDay != NaN) ? totalDay : 0;
        totalAmount.innerText = parseInt(price.innerText.replace(/,/g, "")) * totalDay;
    }
};