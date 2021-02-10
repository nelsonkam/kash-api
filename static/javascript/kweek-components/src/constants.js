export const STRIPE_PUBLIC_KEY =
  location.href.indexOf("localhost") < 0
    ? "pk_live_51HNbkqGCooRhP5Q6UpHWs2xLfN0UZ61K7MJuCyvvWnBhevQFQD3gWh11n4z0b5uIBKTMwpV16rYiRIM0bWS9vfSa00kYS5piE0"
    : "pk_test_51HNbkqGCooRhP5Q61uFIUEgpAPgBaNTxUwoLPIU2wE2YQRlw9jyS0nmz1b4M6DArQzlypqJTPV8jbdrgqP29Md0X00RRTBQzrB";

export const KKIAPAY_API_KEY = location.href.indexOf("localhost") < 0 ? "e586fb90ee0411ea8d5dd1fcfc73e3a8" : "e5ff5fe0ee0411ea86470780f48db989";
