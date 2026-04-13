#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import os
import sys
import random
import argparse
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)
ua = UserAgent()

# إعدادات عامة
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

TIMEOUT = 15

# قائمة APIs تعليمية عامة (غير محددة بكود بلد)
# تقدر تضيف APIs حقيقية خاصة بك لاحقًا
SAMPLE_APIS = [
    # مثال وهمي - غيره بـ APIs حقيقية لو عايز
    {
        "url": "https://example.com/api/send-otp",
        "method": "POST",
        "data": {"phone": "{target}"},
        "success_keywords": ["sent", "success", "otp", "code"]
    },
    # أضف هنا APIs أخرى لو عايز
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.CYAN}   ████████╗███████╗███████╗████████╗███████╗██████╗ 
{Fore.CYAN}   ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
{Fore.GREEN}      ██║   █████╗  ███████╗   ██║   █████╗  ██████╔╝
{Fore.GREEN}      ██║   ██╔══╝  ╚════██║   ██║   ██╔══╝  ██╔══██╗
{Fore.YELLOW}      ██║   ███████╗███████║   ██║   ███████╗██║  ██║
{Fore.YELLOW}      ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{Fore.MAGENTA}                  Mobile Tester v1.0
{Fore.WHITE}        ⚠️ للأغراض التعليمية والاختبار على رقمك الخاص فقط ⚠️
{Style.RESET_ALL}
    """
    print(banner)

def get_headers():
    HEADERS["User-Agent"] = ua.random
    return HEADERS.copy()

def send_request(api_info, target):
    url = api_info["url"].replace("{target}", target)
    headers = get_headers()
    
    try:
        if api_info["method"].upper() == "POST":
            data = {k: v.replace("{target}", target) for k, v in api_info["data"].items()}
            response = requests.post(url, headers=headers, data=data, timeout=TIMEOUT)
        else:
            params = {k: v.replace("{target}", target) for k, v in api_info.get("params", {}).items()}
            response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        
        text = response.text.lower()
        if any(keyword in text for keyword in api_info["success_keywords"]):
            return True
        else:
            return False
    except:
        return False

def print_status(sent, failed, total):
    if total > 0:
        progress = int((sent + failed) / total * 30)
        bar = "█" * progress + "░" * (30 - progress)
        percentage = (sent + failed) / total * 100
    else:
        bar = "░" * 30
        percentage = 0

    status = (
        f"\r{Fore.CYAN}🎯 الهدف: {args.target}   "
        f"{Fore.YELLOW}[{bar}] {percentage:.1f}% ({sent + failed}/{total})\n"
        f"{Fore.GREEN}✅ ناجح: {sent}   "
        f"{Fore.RED}❌ فاشل: {failed}   "
        f"{Fore.MAGENTA}🧵 خيوط: {args.threads}   ⏱ تأخير: {args.delay}s{Style.RESET_ALL}"
    )
    print(status, end="", flush=True)

def start_test():
    print_banner()
    
    if not SAMPLE_APIS:
        print(f"{Fore.RED}[!] لا توجد APIs للاختبار. أضف APIs في SAMPLE_APIS داخل الكود.{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.YELLOW}[*] بدء الاختبار على: {args.target}")
    print(f"{Fore.YELLOW}[*] عدد الطلبات: {args.count} | التأخير: {args.delay}s | الخيوط: {args.threads}\n")
    
    success = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        
        for _ in range(args.count):
            api = random.choice(SAMPLE_APIS)
            futures.append(executor.submit(send_request, api, args.target))
            time.sleep(args.delay)
        
        for future in as_completed(futures):
            if future.result():
                success += 1
            else:
                failed += 1
            print_status(success, failed, args.count)
    
    print("\n\n")
    print(f"{Fore.CYAN}===== انتهى الاختبار =====")
    print(f"{Fore.GREEN}✅ ناجح: {success}")
    print(f"{Fore.RED}❌ فاشل: {failed}")
    print(f"{Fore.YELLOW}📊 إجمالي: {args.count}{Style.RESET_ALL}")

# argparse - كود البلد فارغ تمامًا، تدخل الرقم كامل
parser = argparse.ArgumentParser(description="Mobile Tester - اختبار على رقمك الخاص فقط")
parser.add_argument("-t", "--target", required=True, help="الرقم كامل (مثل 971501234567 أو +971501234567)")
parser.add_argument("-c", "--count", type=int, default=10, help="عدد الطلبات (افتراضي: 10)")
parser.add_argument("-d", "--delay", type=float, default=1.0, help="التأخير بالثواني (افتراضي: 1.0)")
parser.add_argument("-th", "--threads", type=int, default=10, help="عدد الخيوط (افتراضي: 10)")

args = parser.parse_args()

if __name__ == "__main__":
    try:
        start_test()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] تم إيقاف البرنامج{Style.RESET_ALL}")
        sys.exit(0)