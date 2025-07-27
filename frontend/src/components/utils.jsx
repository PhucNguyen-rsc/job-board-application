

function queryToName(slug){
    return slug
    .split('-')                
    .map(word =>           
      word.charAt(0).toUpperCase() + word.slice(1)
    )
    .join(' ');           
}

function validateEmail(email = "") {
    const EMAIL_REGEX = /^(?!.*\.\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/;
    if (email) {
        return EMAIL_REGEX.test(email);
    }
    return false;
}

function isValidPassword(password="") {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
    return passwordRegex.test(password);
  }

const ErrorMessage = ({ message }) => {
    if (!message) return null;

    return (
        <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm mb-4 shadow-sm">
        ⚠️ {message}
        </div>
    );
};

function isConvertibleToInt(str) {
    const num = Number(str);
    return Number.isInteger(num);
  }
  

export {
    queryToName,
    validateEmail,
    isValidPassword,
    ErrorMessage,
    isConvertibleToInt
};