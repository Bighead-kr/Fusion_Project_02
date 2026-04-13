// 1. 함수 앞에 async를 붙여서 비동기 함수로 만들어줍니다.
export default async function CategoryPage({ params }: { params: Promise<{ category: string }> }) {
  // 2. await를 사용해 주소값(params)이 들어올 때까지 잠깐 기다립니다.
  const resolvedParams = await params;
  const currentCategory = resolvedParams.category;

  // 3. 만약 어떤 이유로 카테고리 값이 없다면 에러 대신 안전한 화면을 보여줍니다. (방어 코드)
  if (!currentCategory) {
    return <div className="p-6 text-white">카테고리를 불러오는 중입니다...</div>;
  }

  // 첫 글자만 대문자로 예쁘게 바꿔주기 (tops -> Tops)
  const title = currentCategory.charAt(0).toUpperCase() + currentCategory.slice(1);

  return (
    <div className="p-6 pt-12 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-2">{title}</h1>
      <p className="text-gray-400 mb-8">
        여기는 {title} 아이템들을 모아보는 공간입니다.
      </p>
      
      {/* 나중에 여기에 옷 사진들이 들어갈 임시 격자(Grid) 뼈대 */}
      <div className="grid grid-cols-2 gap-4">
        <div className="h-40 bg-gray-800 rounded-xl animate-pulse"></div>
        <div className="h-40 bg-gray-800 rounded-xl animate-pulse"></div>
        <div className="h-40 bg-gray-800 rounded-xl animate-pulse"></div>
        <div className="h-40 bg-gray-800 rounded-xl animate-pulse"></div>
      </div>
    </div>
  );
}