// let remaining in checkout.html
const customerContainer = document.getElementById('customer-container');
const btnAddCustomer = document.getElementById('btn-add-customer');
const btnDeconsteCustomer = document.getElementById('btn-deconste-customer');
const customerCounterNumber = document.getElementById('customer-counter-number');
const familyMembersCounter = document.getElementById('family-members-counter');

const price = document.getElementById('price');
const dayOfStay = document.getElementById('date-of-stay');
const totalAmount = document.getElementById('total-amount');
const checkInTime = document.getElementById('checkInTime');
const checkOutTime = document.getElementById('checkOutTime');
let count = 0;

function createCustomerBox(index = 0, customerName = '', customerTypes = customerTypesDiv.innerHTML, idCard = '', address = '') {
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
              ${customerTypes}

              <!-- Id  -->
              <div class="md-form md-outline mb-0 mb-lg-4">
                <input type="text" id="idCard[]" name="idCard[]" value="${idCard}" inputmode="numeric" pattern="[0-9\s]{8,12}" class="form-control mb-0 mb-lg-2">
                <label for="idCard[]">CMND / CCCD (8 đến 12 số) (Bỏ trống nếu không có)</label>
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


const DateDiff = {
  inDays: function (d1, d2) {
    let t2 = d2.getTime();
    let t1 = d1.getTime();

    return Math.floor((t2 - t1) / (24 * 3600 * 1000));
  }
};

const numberFormat = {
  withDots: function (n) {
    return n.toLocaleString();
  },
  withCommas: function (n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
}

function getCheckValue() {
  let d1 = new Date(checkInTime.value);
  let d2 = new Date(checkOutTime.value);
  let totalDay = DateDiff.inDays(d1, d2);

  if (!isNaN(d1) && !isNaN(d2)) {
    dayOfStay.innerText = totalDay;
    totalAmount.innerText = numberFormat.withCommas(parseInt(price.innerText.replace(/,/g, "")) * totalDay);
  }
};