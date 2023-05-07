# 시험 응시/관리 프로그램 - 7조 (권인, 김동주, 배계현, 김창용)
# <<< 주석의 위치가 헷갈린다면 왼쪽의 줄 번호를 눌러 한 줄씩 하이라이트 해서 보세요! (VSCode)
       
import oracledb                                                                 # oracledb 모듈 가져오기
from oracledb import exceptions                                                 # oracledb의 exceptions(예외) 가져오기
oracledb.init_oracle_client()                                                   # oracledb 초기화

# 1-1. 테이블 생성 : 수험자 정보
try:                                                                            # 'try~except~': 테이블 생성 시 중복 오류 예외 처리
    conn = oracledb.connect('SCOTT/TIGER@localhost:1521/xe')                    # oracle db에 연결
    cur = conn.cursor()                                                         # cursor 객체 생성
    sql = 'create table examinee_info(ex_num varchar2(50) primary key, name varchar2(10), gender varchar2(10), sub_num number)'
     # 쿼리문 작성 : 테이블 생성 (이름 : examinee_info(수험자 정보), column : 수험번호, 이름, 성별(가변형 문자열), 과목코드(숫자))
    cur.execute(sql)                                                            # 쿼리문 실행
    conn.commit()                                                               # 작업 변경 사항 저장
except Exception as e:                                                          # Exception : 모든 오류에 대한 예외 처리
    pass                                                                        # 중복 오류에 대한 예외 처리 : 통과

# 1-2. 테이블 생성 : 시험 정보
try:                                                                            # 'try~except~': 테이블 생성 시 중복 오류 예외 처리
    sql = 'create table test_info(sub_num number, loc varchar2(10), time varchar2(10))'
     # 쿼리문 작성 : 테이블 생성 (이름 : test_info(시험 정보), column : 과목코드(숫자), 시험장소, 시험시간(가변형 문자열))
    cur.execute(sql)                                                            # 쿼리문 실행
    conn.commit()                                                               # 작업 변경 사항 저장
except Exception as e:                                                          # Exception : 모든 오류에 대한 예외 처리
    pass                                                                        # 중복 오류에 대한 예외 처리 : 통과

# 1-3. 테이블 생성 : 관리자 정보
try:                                                                            # 'try~except~': 테이블 생성 시 중복 오류 예외 처리
    sql = 'create table manager_info (name varchar2(10), mgr_id varchar2(10) primary key, mgr_pw varchar2(15))'
     # 쿼리문 작성 : 테이블 생성 (이름 : manager_info(관리자 정보), column : 이름, ID, 비밀번호(가변형 문자열))
    cur.execute(sql)                                                            # 쿼리문 실행
    conn.commit()                                                               # 작업 변경 사항 저장
except Exception as e:                                                          # Exception : 모든 오류에 대한 예외 처리
    pass                                                                        # 중복 오류에 대한 예외 처리 : 통과

# 1-4. 테이블 생성 : 문제 목록, 답 목록 
try:                                                                            # 'try~except~': 테이블 생성 시 중복 오류 예외 처리
    sql = 'create table probs (sub_num number primary key)'                 
    # 쿼리문 작성 : 테이블 생성 (이름 : probs(문제 목록), column : 과목코드(숫자))
    cur.execute(sql)                                                            # 쿼리문 실행
    sql = 'create table ans (sub_num number primary key)'
    # 쿼리문 작성 : 테이블 생성 (이름 : ans(답 목록), column : 과목코드(숫자))
    cur.execute(sql)                                                            # 쿼리문 실행
    for i in range(5):                                                          # 반복문 : 5회 실행 (i : 0 ~ 4)
        sql = f'ALTER TABLE probs ADD NO{i+1} VARCHAR2(255)'      
        # 쿼리문 작성 : column 추가(테이블 probs에 추가), f-string 사용 (i+1) '예) column 이름 : NO1, NO2,..., NO5'
        cur.execute(sql)                                                        # 쿼리문 실행
        sql = f'ALTER TABLE ans ADD NO{i+1} VARCHAR2(255)'
        # 쿼리문 작성 : column 추가(테이블 ans에 추가), f-string 사용 (i+1) '예) column 이름 : NO1, NO2,..., NO5'
        cur.execute(sql)                                                        # 쿼리문 실행
    conn.commit()                                                               # 작업 변경 사항 저장
except Exception as e:                                                          # Exception : 모든 오류에 대한 예외 처리
    pass                                                                        # 중복 오류에 대한 예외 처리 : 통과

# 1-5. 테이블 생성 : 응시 결과
try:                                                                            # 'try~except~': 테이블 생성 시 중복 오류 예외 처리
    sql = 'create table pfs (ex_num varchar2(10) primary key, pf varchar2(50), sub_num number, score_num number)'
    # 쿼리문 작성 : 테이블 생성 (이름 : pfs(응시 결과), column : 수험번호, 합격여부(가변형 문자열), 과목코드(숫자), 점수(숫자))
    # ex_num > primary key : 여기에 중복 또는 NULL 값 입력 시 오류 발생
    cur.execute(sql)                                                            # 쿼리문 실행
    conn.commit()                                                               # 작업 변경 사항 저장
    conn.close()                                                                # oracle db 연결 해제
except Exception as e:                                                          # Exception : 모든 오류에 대한 예외 처리
    pass                                                                        # 중복 오류에 대한 예외 처리 : 통과
print('{0:*^40}'.format('시험 응시 프로그램'))

# 2. 로그인
while True:                                                                     # 반복문 : 프로그램 계속 실행
    with oracledb.connect('SCOTT/TIGER@localhost:1521/xe') as conn:             # oracle db에 연결 (with : conn.close() 사용 X)
        with conn.cursor() as cur:                                              # cursor 객체 생성 (with : conn.close() 사용 X)
            sql = 'select ex_num from examinee_info'
            # 쿼리문 작성 : 데이터 가져오기 (수험자리스트(examinee_info)에서 모든 수험번호(ex_num) 가져오기)
            cur.execute(sql)                                                    # 쿼리문 실행
            ex_num_list = [x[0] for x in cur.fetchall()]
            # 수험번호 리스트 생성 : cur.fetchall()시 ('수험번호',) 형태로 출력되므로 첫번째 값 인덱싱 반복하여 리스트 생성 (list comprehension 사용)
            print('수험번호를 입력하세요')
            logon = input('(종료하려면 q를 누르세요.)\n')
            # 변수 생성 : 수험번호를 입력받아 저장하는 변수 생성 
            # 관리자 모드 : 회원 가입 (관리자 정보 추가)
            if logon == 'I':                                                     # 수험번호가 아닌 특수한 값(I)인 경우 : 회원가입
                # 추가할 관리자 정보 입력
                print('--- 관리자 모드 : 회원가입 ---')                          # 관리자 모드 진입을 알려줌
                name = input('이름을 입력하세요.\n')                             # 이름 입력
                id = input('ID를 입력하세요.\n')                                 # ID 입력
                pw = input('비밀번호를 입력하세요.\n')                           # 비밀번호 입력
                sql = 'insert into manager_info values(:1,:2,:3)'              
                # 쿼리문 작성 : 관리자 리스트에 입력받은 값 추가
                try:
                    cur.execute(sql,(name,id,pw))                                # 쿼리문 실행
                    conn.commit()                                                # 작업 변경 사항 저장
                    print('생성되었습니다.')                                     # 추가 완료됨을 알려주는 메시지 출력
                except Exception as e:                                           # 중복 오류(mgr_id에 입력되는 id값) 발생 시 출력
                    print('존재하는 ID입니다. 다시 시도하세요.')
                continue                                                        # 회원가입 후 초기화면으로 돌아가기
            
            # 관리자 모드 : 로그인
            elif logon == 'A':                                                  # 수험번호가 아닌 특수한 값(A)인 경우 : 관리자 모드
                print('---- 관리자 모드 : 로그인 ---')                           # 관리자 모드 진입을 알려줌 
                while True:                                                     # 반복문 : 로그인 시도 반복
                    sql = 'select mgr_id from manager_info'
                    # 쿼리문 작성 : 관리자리스트에서 ID 가져오기
                    cur.execute(sql)                                            # 쿼리문 실행
                    mgr_id_list = [x[0] for x in cur.fetchall()]
                    # ID 리스트 생성 : cur.fetchall()시 ('ID',) 형태로 출력되므로 첫번째 값 인덱싱 반복하여 리스트 생성 (list comprehension 사용)
                    manager_id = input('ID를 입력하세요.\n')                    # 찾을(로그인 할) ID 입력
                    manager_pw = input('비밀번호를 입력하세요.\n')              # 찾을(로그인 할) 비밀번호 입력
                    if manager_id in mgr_id_list:                               # 조건문 : 입력받은 ID가 ID 리스트에 있을 경우
                        sql = 'select mgr_pw from manager_info where mgr_id=:1'
                        # 쿼리문 작성 : 관리자리스트에서 입력받은 ID에 해당하는 비밀번호 가져오기
                        cur.execute(sql,(manager_id,))                          # 쿼리문 실행
                        password = cur.fetchone()[0]                            # 가져온 값을 변수에 저장
                        if manager_pw == password:                              # 조건문 : ID 리스트(테이블) 속 동일한 ID의 비밀번호와 입력한 비밀번호가 같을 경우
                            sql = 'select name from manager_info where mgr_id=:1'
                            # 쿼리문 작성 : 관리자리스트에서 입력받은 ID에 해당하는 이름 가져오기
                            cur.execute(sql,(manager_id,))                      # 쿼리문 실행
                            mgr_name = cur.fetchone()[0]                        # 가져온 값을 변수에 저장
                            print(f'--- {mgr_name}님 환영합니다. ---')          # 로그인 성공을 알려줌
                            logon = 'M'                                         # 관리자 모드로 넘어가기 위한 새로운 값 저장
                            break                                               # 로그인 시도 종료
                        else:                                                   # 조건문 : 비밀번호가 같지 않을 경우
                            print('잘못된 비밀번호를 입력하셨습니다.')          # 비밀번호가 잘못 입력됨을 알려줌
                    else:                                                       # 조건문 : 입력받은 ID가 ID 리스트에 없을 경우
                        print('등록되지 않은 정보입니다.')                      # 관리자 정보가 없음을 출력
                        break                                                   # 비밀번호 시도 중지(빠져나가기)
                
# 3-1. 관리자 
    if logon == 'M':                                                            # 로그인 성공 : 변수(logon)의 값이 M으로 바뀐 경우
        with oracledb.connect('SCOTT/TIGER@localhost:1521/xe') as conn:         # oracle db에 연결 (with : conn.close() 사용 X)
            with conn.cursor() as cur:                                          # cursor 객체 생성 (with : conn.close() 사용 X)
                while True:                                                     # 반복문 : 메뉴 고르기 시작
                    menu = input('  선택하세요.\n(1) 인적사항 입력\n(2) 인적사항 조회\n(3) 시험정보 입력\n(4) 문제와 답 입력\n(5) 시험결과확인\n(q) 종료\n')
                    if menu == '1':                                             # 1이 입력된 경우 : 수험자 인적사항 입력       
                                try: 
                                    test_num = input('수험번호\n')               # 수험번호 입력
                                    name = input('이름\n')                       # 이름 입력
                                    gender = input('성별\n')                     # 성별 입력
                                    sub_num = int(input('과목코드\n'))           # 과목코드 입력           
                                    sql = f'insert into examinee_info values(:1,:2,:3,:4)'
                                    # 쿼리문 작성 : 수험자리스트에 입력받은 값 추가
                                    cur.execute(sql,(test_num,name,gender,sub_num)) # 쿼리문 실행
                                    conn.commit()                                   # 작업 변경 사항 저장 
                                except exceptions.IntegrityError:                   # 수험번호에서 발생하는 무결성 오류(중복, NULL)에 대한 예외 처리
                                    print('잘못된 수험번호입니다.')  
                                except Exception as e:                              # 기타 오류(sub_num에 int()에 값이 들어가지 않은 경우)에 대한 예외 처리
                                    print('다시 입력해주십시오.')                                                                           
                    
                    elif menu == '2':                                           # 2가 입력된 경우 : 수험자 인적 사항 조회
                        while True:                                             # 반복문 : 수험자 검색 시작
                            exm = input('--- 수험자 인적사항 조회 ---\n(1) 수험생 검색 (2) 전체 조회 (q) 종료\n')  
                            # 검색할 대상 입력 : 전체 수험자 정보 테이블 / 수험자 1명
                            if exm == '1':                                      # '수험생 1명'일 경우  
                                key = input('수험번호를 입력하세요\n')          # 찾고자하는 수험생의 수험번호 입력
                                cur.execute('select * from examinee_info where ex_num=:1',(key,))
                                # 쿼리문 작성 : 수험자 정보 테이블에서 입력받은 수험번호에 해당하는 정보 가져오기
                                examinee = cur.fetchone()
                                print(f'수험번호 : {examinee[0]} 이름 : {examinee[1]} 성별 : {examinee[2]} 과목코드 : {examinee[3]}')   # 가져온 정보 출력                        
                            elif exm == '2':                                    # 수험생 전체의 리스트일 경우
                                key = input('정렬기준선택\n(1) 수험번호 (2) 이름 (3) 과목코드\n')
                                if key == '1':                                  # 조건문 : 정렬 기준 입력에 따른 값(쿼리문에 넣을) 변수에 저장
                                    key = 'ex_num'
                                elif key == '2':
                                    key = 'name'
                                elif key == '3':
                                    key = 'sub_num'
                                else:                                           # 다른 값을 입력했을 경우 이전화면으로
                                    print('다시 시도하세요, 이전으로 돌아갑니다.')
                                    continue
                                sort = input('정렬방향선택\n(1) 오름차순 (2) 내림차순\n')
                                if sort == '1':                                 # 조건문 : 정렬 방향 입력에 따른 값(쿼리문에 넣을) 변수에 저장
                                    sort = 'asc'
                                elif sort == '2':
                                    sort = 'desc'
                                else:                                           # 다른 값을 입력했을 경우 이전화면으로
                                    print('다시 시도하세요, 이전으로 돌아갑니다.')
                                    continue
                                sql=f'select * from examinee_info order by {key} {sort}'
                                # 쿼리문 작성 : key값을 기준으로, sort값을 방향으로 하여 정렬된 수험자 정보 테이블 가져오기
                                for item in cur.execute(sql):                   # 반복문 : 가져온 데이터 출력
                                    print(f'수험번호 : {item[0]} 이름 : {item[1]} 성별 : {item[2]} 과목코드 : {item[3]}')
                                    # item : (수험번호,이름,성별,과목코드) 이므로 인덱싱 하여 값 호출, 출력
                            elif exm in ('q','Q','ㅂ'):                         # 종료하는 경우
                                print('수험자 인적사항 조회를 종료합니다.')     # 종료메시지 출력
                                break                                           # 수험자 인적사항 조회 중지(빠져나가기)
                            else:                                               # 다른 값을 입력한 경우      
                                print('잘못 입력하셨습니다.')                   # 알림 메시지 출력
                    
                    elif menu == '3':                                           # 3이 입력된 경우 : 시험 정보 입력(추가)                                      
                        sub_num = int(input('과목코드\n'))                      # 과목코드 입력
                        loc = input('고사장\n')                                 # 고사장 입력
                        time = input('시험시간\n')                              # 시험시간 입력
                        sql = 'insert into test_info values(:1,:2,:3)'
                        # 쿼리문 작성 : 시험정보 테이블에 입력받은 값 추가
                        cur.execute(sql,(sub_num,loc,time))                     # 쿼리문 실행
                        conn.commit()                                           # 작업 변경 사항 저장
                        print('시험이 생성되었습니다.')                         # 알림 메시지 출력
                    
                    elif menu == '4':                                           # 4가 입력된 경우 : 시험 문제, 답 입력
                        subnum = int(input('생성할 시험의 과목코드를 입력하세요.\n')) # 과목코드 입력받기
                        pros = []                                               # 입력받은 값 담을 문제 리스트 생성
                        solves = []                                             # 입력받은 값 담을 답 리스트 생성
                        for i in range(5):                                      # 반복문 : 5회 반복
                            pro = input(f'{i+1}번 문제를 입력하세요.\n')          # 문제 내용 입력받기, f-string으로 문제 번호를 바꾸며 입력 프롬프트 출력
                            pros.append(pro)                                    # 문제 리스트에 입력받은 내용추가
                            sol = input(f'{i+1}번 문제의 답을 입력하세요.\n')    # 답 내용 입력받기, f-string으로 답 번호를 바꾸며 입력 프롬프트 출력
                            solves.append(sol)                                  # 문제 리스트에 입력받은 내용추가
                        sql = f'insert into probs values({subnum},:1,:2,:3,:4,:5)'
                        # 쿼리문 작성 : 문제 테이블에 입력받은 정보 추가 (과목코드, 5개의 문제)
                        try:
                            cur.execute(sql,tuple(pros))                            # 쿼리문 실행 (pros : list -> tuple)
                            sql = f'insert into ans values({subnum},:1,:2,:3,:4,:5)'
                            # 쿼리문 작성 : 문제 테이블에 입력받은 정보 추가 (과목코드, 5개의 문제)
                            cur.execute(sql,tuple(solves))                          # 쿼리문 실행 (ans : list -> tuple)
                            conn.commit()                                           # 작업 변경 사항 저장
                        except exceptions.IntegrityError:                           # 과목코드(PK)로 인한 오류 예외처리
                            print('중복된 과목코드입니다.')  
                        except Exception as e:                                      # 기타 오류 예외처리
                            print('다시 입력해주십시오.')   
                    
                    elif menu == '5':                                               # 5가 입력된 경우 : 특정 시험을 본 학생들의 결과 조회
                        num = int(input('조회할 과목 코드를 입력하세요.\n'))        # 과목코드 입력
                        sql = 'select * from pfs where sub_num = :1'        
                        # 쿼리문 작성 : 응시 결과 테이블에서 해당하는 과목코드의 데이터를 가져오기
                        try:
                            cur.execute(sql,(num,))                                 # 쿼리문 실행
                            for i in cur.fetchall():                                # 반복문 : 가져온 데이터 하나씩 호출하기
                                print(f'수험번호 : {i[0]} 결과 : {i[1]} 과목코드 : {i[2]} 점수 : {i[3]}')
                                # 호출한 데이터 : (수험번호, 합격여부, 과목코드) 이므로 하나씩 인덱싱해서 출력
                        except Exception as e:                                  # 오류 예외 처리
                            print('정보가 없습니다.')
                    
                    elif menu in ('q','Q','ㅂ'):                                # q(Q,ㅂ)가 입력된 경우 : 종료
                        print('로그아웃합니다.')                                # 종료메시지 출력
                        break                                                   # 시험결과조회 종료 (빠져나가기)
                    
                    else:                                                       # 다른 값이 입력된 경우             
                        print('다시 입력하세요')                                # 메시지 출력 : 메뉴에 나와있는 값을 입력하도록 유도

# 3-2. 수험자
    elif logon in ex_num_list:                                                  # 입력받은 값(logon)이 수험번호 리스트에 있는 경우
        print('--- 수험자 로그인 ---')                                                  # 메시지 출력 : 수험자 모드 진입 알림
        ex_key = logon                                                          # 현재 수험자를 인식할 수 있게 수험번호 다른 변수에 저장
        with oracledb.connect('SCOTT/TIGER@localhost:1521/xe') as conn:         # oracle db에 연결 (with : conn.close() 사용 X)
            with conn.cursor() as cur:                                          # cursor 객체 생성 (with : conn.close() 사용 X)      
                while True:                                                     # 반복문 : 메뉴 고르기 시작
                    menu = input('  선택하세요.\n(1) 인적사항 조회\n(2) 응시결과 조회\n(3) 시험 응시\n(q) 종료\n')
                    if menu == '1':                                             # 1이 입력된 경우 : 수험자 본인 인적사항 조회
                        try: 
                            cur.execute('select * from examinee_info where ex_num=:1',(ex_key,))
                            #  쿼리문 실행 : 
                            a = cur.fetchone()                                  # 가져온 데이터 '(수험번호, 이름, 성별, 과목코드)' 변수에 저장
                            print(f'수험번호 : {a[0]} 이름 : {a[1]} 성별 : {a[2]}')
                            # 데이터 인덱싱 하여 출력 (과목코드 제외!)
                            cur.execute('select sub_num from examinee_info where ex_num =:1',(ex_key,))
                            #  쿼리문 실행 : 수험자목록 테이블에서 저장된 수험번호에 해당하는 과목코드 가져오기
                            b = cur.fetchone()[0]                               # 가져온 데이터 '(과목코드,)'의 첫번째 값 '과목코드' 변수에 저장
                            cur.execute('select * from test_info where sub_num=:1',(b,))
                            #  쿼리문 실행 : 변수에 저장된 값과 같은 과목코드를 가진 데이터(행)을 시험정보 테이블에서 가져오기
                            c = cur.fetchall()[0]                               # 가져온 데이터 '(과목코드,시험장소,시험시간)'의 첫번째 값 변수에 저장
                            print(f'시험시간 : {c[2]} 시험장소 : {c[1]}')
                            # 변수에 저장된 데이터를 인덱싱하여 해당 시험의 시간과 장소 출력
                        except Exception as e:                                  # 오류 예외 처리
                            print('시험정보를 입력해주세요.')
    
                    elif menu == '2':                                           # 2가 입력된 경우 : 수험자의 응시 결과 조회
                        try:
                            result = list(cur.execute('select * from pfs where ex_num = :1',(ex_key,)))[0]
                            # 쿼리문 실행 : 응시결과 테이블에서 저장된 수험번호에 해당하는 데이터 가져오기
                            # 가져온 데이터를 리스트로 변환하고 인덱싱하여 첫 번째 값 변수에 저장
                            # result = [수험번호, 합격여부, 과목코드]
                            print(f'{result[0]}번 수험생은 {result[3]}점으로 {result[1]}하셨습니다.')
                            # 변수(result)에 저장된 값 인덱싱해서 응시 결과 출력
                        except Exception as e:                                  # 오류 예외 처리
                            print('정보가 없습니다.')
                    
                    elif menu == '3':                                           # 3이 입력된 경우 : 시험 응시
                        sql = 'select sub_num from examinee_info where ex_num=:1'
                        # 쿼리문 작성 : 수험자목록 테이블에서 저장된 수험번호에 해당하는 데이터의 과목코드 가져오기
                        cur.execute(sql,(ex_key,))                              # 쿼리문 실행
                        num = cur.fetchone()[0]                                 # 가져온 데이터 '(과목코드,)' 의 첫 번째 원소 변수에 저장
                        try:
                            cur.execute('select pf from pfs where ex_num = :1',(ex_key,))
                            # 쿼리문 실행 : 현재 수험자의 수험번호에 해당하는 합격여부 정보 응시결과 테이블에서 가져오기
                            test_result = cur.fetchone()[0]                     # '합격'/'불합격'값 변수에 저장
                            if test_result in ('합격','불합격'):                # 조건문 : '합격'/'불합격'일 경우
                                print('이미 응시했습니다.')                     # 알림 메시지 출력
                                print('로그아웃합니다.')                        
                                break                                           # 수험번호 입력화면으로 돌아가기
                        except Exception as e:                                  # 미응시인 경우 발생하는 오류 예외 처리
                            pass
                        sql = 'select * from probs where sub_num = :1'
                        # 쿼리문 작성 : 문제 테이블에서 저장된 과목코드에 해당하는 데이터 가져오기
                        cur.execute(sql,(num,))                                 # 쿼리문 실행
                        probs = cur.fetchall()                                  # 가져온 데이터 '[(과목코드,1번문제,2번문제,3번문제,4번문제,5번문제)]' 변수에 저장
                        sql = 'select * from ans where sub_num = :1'
                        # 쿼리문 작성 : 답 테이블에서 저장된 과목코드에 해당하는 데이터 가져오기
                        cur.execute(sql,(num,))                                 # 쿼리문 실행
                        ans = cur.fetchall()                                    # 가져온 데이터 '(과목코드,1번답,2번답,3번답,4번답,5번답) 변수에 저장
                        count = 0                                               # 정답 갯수를 체크할 변수 생성, 0으로 초기화
                        for i in range(len(probs)):                             # 반복문 : 1회 반복 / probs = [(과목코드,1번문제,..,5번문제)] 이므로 len(probs) = 1
                            for j in range(1,len(probs[i])):                    # 중첩 반복문 : 1~5, 5회 반복 / probs[i] = (과목코드,1번문제,..,5번문제) 이므로 과목코드 제외한 나머지 문제 인덱싱
                                a = input(f'{probs[i][j]}\n정답을 입력하시오.\n')# 답 입력 / f-string으로 인덱싱한 값(문제) 출력
                                if a == ans[i][j]:                              # 조건문 : 입력받은 값이 답리스트에 있는 문제리스트와 동일한 인덱스(위치)의 값과 같은지 확인
                                    count += 1                                  # 같다면 정답 갯수 체크하는 변수에 + 1
                        if count >=4:                                           # 조건문 : 반복문 종료 후 정답 갯수 체크 변수에 저장된 값(정답 갯수) 가 커트라인(4) 이상인지 확인
                            cur.execute('insert into pfs values(:1,:2,:3,:4)',(ex_key,'합격',num,count*20))
                            # 쿼리문 실행 : 응시결과 테이블에 수험번호,합격,과목코드 추가
                            conn.commit()                                       # 작업 변경 사항 저장
                        else:                                                   # count(정답 갯수) < 4 인 경우
                            cur.execute('insert into pfs values(:1,:2,:3,:4)',(ex_key,'불합격',num,count*20))
                            # 쿼리문 실행 : 응시결과 테이블에 수험번호,합격,과목코드 추가
                            conn.commit()                                       # 작업 변경 사항 저장
                    
                    elif menu in ('q','Q','ㅂ'):                                # q(Q,ㅂ)이 입력된 경우 : 종료
                        print('로그아웃합니다.')                                # 종료메시지 출력
                        break                                                   # 수험자 모드 종료(빠져나가기)
                    
                    else:                                                       # 그 외 다른 값이 입력된 경우
                        print('다시 입력하세요')                                # 메시지 출력 : 메뉴에 나와있는 값을 입력하도록 유도
   
    elif logon in ('q','Q','ㅂ'):                                               # 수험번호 입력 단계에서 q(Q,ㅂ)가 입력된 경우 : 프로그램 종료
        print('프로그램을 종료합니다.')                                         # 종료메시지 출력
        break                                                                   # 프로그램 종료
   
    else:                                                                       # 그 외 다른 값이 입력된 경우
        print('잘못된 정보입니다.')                                             # 메시지 출력 : 정확한 값 입력 유도