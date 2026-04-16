import zipfile
import json
import os

def convert_aihub_zip_to_reference(zip_path, output_file):
    final_data = []
    
    if not os.path.exists(zip_path):
        print(f"❌ '{zip_path}' 파일을 찾을 수 없습니다.")
        return

    print(f"📦 {zip_path} 분석 시작...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            json_files = [f for f in z.namelist() if f.endswith('.json')]
            print(f"📄 총 {len(json_files)}개의 파일을 찾았습니다. 변환을 시작합니다.")

            for i, file_name in enumerate(json_files):
                try:
                    with z.open(file_name) as f:
                        # 1. 인코딩 확인 및 로드
                        content = f.read().decode('utf-8-sig')
                        raw_data = json.loads(content)
                        
                        # 2. 데이터 깊은 곳까지 찾아 들어가기 (수정된 부분)
                        # 데이터셋 정보 -> 데이터셋 상세설명 -> 라벨링
                        base_info = raw_data.get('데이터셋 정보', {})
                        detail_info = base_info.get('데이터셋 상세설명', {})
                        labeling = detail_info.get('라벨링', {})
                        
                        if not labeling: # 혹시 위 경로가 아니면 바로 아래 '라벨링' 확인
                            labeling = base_info.get('라벨링', {})

                        # 3. 스타일 및 아이템 추출
                        style_list = labeling.get('스타일', [{}])
                        main_style = style_list[0].get('스타일', '기본 스타일')
                        
                        items = []
                        for cat in ['상의', '하의', '아우터', '원피스']:
                            if cat in labeling and isinstance(labeling[cat], list):
                                item_info = labeling[cat][0]
                                if '카테고리' in item_info and item_info['카테고리']: # 데이터가 있는 경우만
                                    items.append({
                                        "category": cat,
                                        "sub_category": item_info.get('카테고리', '기타'),
                                        "color": item_info.get('색상', '미상'),
                                        "formal_level": 3
                                    })
                        
                        # 4. 결과 저장
                        if items:
                            final_data.append({
                                "set_name": f"{main_style} 코디",
                                "situation": "일상",
                                "temp_range": [10, 20],
                                "items": items
                            })
                            
                except Exception:
                    continue
                
                if (i + 1) % 1000 == 0:
                    print(f"🔄 {i + 1}개 완료... (현재까지 {len(final_data)}개 성공)")

        # 최종 저장
        with open(output_file, 'w', encoding='utf-8') as out:
            json.dump(final_data, out, indent=4, ensure_ascii=False)
        
        print(f"\n✅ 드디어 변환 성공!")
        print(f"✨ 총 {len(final_data)}개의 전문가 코디가 저장되었습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

# 실행 (파일명 주의!)
zip_name = "라벨링데이터.zip.part0" 
output_name = "reference_fashion.json"
convert_aihub_zip_to_reference(zip_name, output_name)